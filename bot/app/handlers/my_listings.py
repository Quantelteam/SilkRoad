import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import db
from app.config import MAX_PHOTOS
from app.filters import PLAIN_TEXT
from app.handlers.parts_picker import RESOLVERS, ask_part
from app.i18n import t
from app.keyboards import (MY_LISTINGS, condition_kb, edit_menu_kb, listing_actions_kb,
                           main_menu, note_kb, photos_kb, price_kb)
from app.photos import upload_telegram_photos
from app.states import EditListing
from app.texts import format_listing

router = Router()

MAX_NOTE = 300
MAX_PRICE = 100_000_000


@router.message(F.text.in_(MY_LISTINGS))
async def my_listings(message: Message, state: FSMContext, user: dict | None, lang: str) -> None:
    if not user:
        await message.answer(t("register_first", lang))
        return
    await state.clear()
    listings = await db.user_listings(message.from_user.id)
    if not listings:
        await message.answer(t("no_listings", lang), reply_markup=main_menu(lang))
        return
    for listing in listings:
        await message.answer(format_listing(listing, lang),
                             reply_markup=listing_actions_kb(listing["id"], lang))


async def _send_listing(message: Message, listing_id: int, tg_id: int, lang: str) -> None:
    listing = await db.get_listing(listing_id, tg_id)
    if listing is None:
        await message.answer(t("listing_gone", lang))
        return
    await message.answer(format_listing(listing, lang),
                         reply_markup=listing_actions_kb(listing_id, lang))


# --- close -----------------------------------------------------------------

@router.callback_query(F.data.startswith("close:"))
async def close_listing(call: CallbackQuery, lang: str) -> None:
    listing_id = int(call.data.split(":")[1])
    listing = await db.update_listing(listing_id, call.from_user.id, {"status": "closed"})
    if listing is None:
        await call.answer(t("not_yours", lang), show_alert=True)
        return
    await call.message.edit_text(t("listing_closed", lang, id=listing_id))
    await call.answer()


# --- edit ------------------------------------------------------------------

@router.callback_query(F.data.startswith("edit:"))
async def edit_listing(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    listing_id = int(call.data.split(":")[1])
    listing = await db.get_listing(listing_id, call.from_user.id)
    if listing is None:
        await call.answer(t("not_yours", lang), show_alert=True)
        return
    await state.clear()
    await state.set_state(EditListing.menu)
    await state.update_data(listing_id=listing_id, type=listing["type"],
                            tg_id=call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=edit_menu_kb(listing, lang))
    await call.answer()


@router.callback_query(EditListing.menu, F.data.startswith("ef:"))
async def edit_field(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    _, field, raw_id = call.data.split(":")
    listing_id = int(raw_id)
    data = await state.get_data()
    kind = data.get("type")

    if field == "back":
        await state.clear()
        await call.message.edit_reply_markup(reply_markup=listing_actions_kb(listing_id, lang))
        await call.answer()
        return

    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()

    if field == "part":
        prompt = t("edit_part_wanted" if kind == "wanted" else "edit_part_have", lang)
        await ask_part(call.message, state, prompt, "edit_part", EditListing.part, lang)
    elif field == "price":
        await state.set_state(EditListing.price)
        await call.message.answer(t("edit_price", lang), reply_markup=price_kb(lang))
    elif field == "cond":
        await state.set_state(EditListing.condition)
        await call.message.answer(t("edit_condition", lang), reply_markup=condition_kb(lang))
    elif field == "note":
        await state.set_state(EditListing.note)
        await call.message.answer(t("edit_note", lang), reply_markup=note_kb(lang))
    elif field == "photos":
        await state.set_state(EditListing.photos)
        await state.update_data(photo_ids=[])
        await call.message.answer(t("edit_photos", lang, max=MAX_PHOTOS),
                                  reply_markup=photos_kb(0, lang))


async def _apply(message: Message, state: FSMContext, fields: dict, lang: str) -> None:
    data = await state.get_data()
    listing_id, tg_id = data["listing_id"], data["tg_id"]
    updated = await db.update_listing(listing_id, tg_id, fields)
    await state.clear()
    if updated is None:
        await message.answer(t("listing_gone", lang))
        return
    await _send_listing(message, listing_id, tg_id, lang)


async def _resolve_edit_part(message: Message, state: FSMContext,
                             part: dict | None, text: str | None, lang: str) -> None:
    data = await state.get_data()
    side = "want" if data.get("type") == "wanted" else "have"
    await _apply(message, state, {
        f"{side}_part_id": part["id"] if part else None,
        f"{side}_text": text,
    }, lang)


RESOLVERS["edit_part"] = _resolve_edit_part


@router.message(EditListing.price, PLAIN_TEXT)
async def edit_price(message: Message, state: FSMContext, lang: str) -> None:
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) > MAX_PRICE:
        await message.answer(t("bad_price", lang))
        return
    await _apply(message, state, {"price_kzt": int(raw)}, lang)


@router.callback_query(EditListing.price, F.data == "price:any")
async def edit_price_negotiable(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await call.message.edit_text(t("price_set_negotiable", lang))
    await call.answer()
    await _apply(call.message, state, {"price_kzt": None}, lang)


@router.callback_query(EditListing.condition, F.data.startswith("cond:"))
async def edit_condition(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _apply(call.message, state, {"condition": call.data.split(":")[1]}, lang)


@router.message(EditListing.note, PLAIN_TEXT)
async def edit_note(message: Message, state: FSMContext, lang: str) -> None:
    note = message.text.strip()
    if len(note) > MAX_NOTE:
        await message.answer(t("note_too_long", lang, max=MAX_NOTE))
        return
    await _apply(message, state, {"note": note}, lang)


@router.callback_query(EditListing.note, F.data == "note:skip")
async def clear_note(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _apply(call.message, state, {"note": None}, lang)


@router.message(EditListing.photos, F.photo)
async def edit_add_photo(message: Message, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    if len(photo_ids) >= MAX_PHOTOS:
        await message.answer(t("photo_limit", lang, max=MAX_PHOTOS),
                             reply_markup=photos_kb(len(photo_ids), lang))
        return
    photo_ids.append(message.photo[-1].file_id)
    await state.update_data(photo_ids=photo_ids)
    await message.answer(t("photo_added", lang, count=len(photo_ids), max=MAX_PHOTOS),
                         reply_markup=photos_kb(len(photo_ids), lang))


@router.callback_query(EditListing.photos, F.data == "photos:done")
async def edit_photos_done(call: CallbackQuery, state: FSMContext, bot: Bot, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    urls: list[str] = []
    if photo_ids:
        try:
            urls = await upload_telegram_photos(bot, photo_ids)
        except Exception:
            logging.exception("photo upload failed")
            await call.message.answer(t("photos_failed_nothing", lang))
            await state.clear()
            return
    await _apply(call.message, state, {"photos": urls}, lang)
