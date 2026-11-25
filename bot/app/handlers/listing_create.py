import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import db
from app.config import MAX_PHOTOS
from app.filters import PLAIN_TEXT
from app.handlers.parts_picker import RESOLVERS, ask_part
from app.i18n import t
from app.keyboards import (NEW_LISTING, website_kb, condition_kb, confirm_kb, listing_type_kb,
                           main_menu, note_kb, photos_kb, price_kb)
from app.photos import upload_telegram_photos
from app.states import NewListing
from app.texts import format_listing

router = Router()

MAX_NOTE = 300
MAX_PRICE = 100_000_000


@router.message(F.text.in_(NEW_LISTING))
async def new_listing(message: Message, state: FSMContext, user: dict | None, lang: str) -> None:
    if not user:
        await message.answer(t("register_first", lang))
        return
    await state.clear()
    await state.set_state(NewListing.type)
    await message.answer(t("ask_listing_type", lang), reply_markup=listing_type_kb(lang))


@router.callback_query(NewListing.type, F.data.startswith("type:"))
async def pick_type(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    kind = call.data.split(":")[1]
    await state.update_data(type=kind)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    prompt = t("ask_part_wanted" if kind == "wanted" else "ask_part_have", lang)
    await ask_part(call.message, state, prompt, "create_main", NewListing.part, lang)


async def _resolve_main(message: Message, state: FSMContext,
                        part: dict | None, text: str | None, lang: str) -> None:
    data = await state.get_data()
    kind = data["type"]
    side = "want" if kind == "wanted" else "have"
    await state.update_data(**{f"{side}_part": part, f"{side}_text": text})

    if kind == "trade":
        await ask_part(message, state, t("ask_part_return", lang),
                       "create_want", NewListing.part, lang)
    elif kind == "sell":
        await state.set_state(NewListing.price)
        await message.answer(t("ask_price", lang), reply_markup=price_kb(lang))
    elif kind == "give":
        await _ask_condition(message, state, lang)
    else:
        await _ask_photos(message, state, lang)


async def _resolve_want(message: Message, state: FSMContext,
                        part: dict | None, text: str | None, lang: str) -> None:
    await state.update_data(want_part=part, want_text=text)
    await _ask_condition(message, state, lang)


RESOLVERS["create_main"] = _resolve_main
RESOLVERS["create_want"] = _resolve_want


async def _ask_condition(message: Message, state: FSMContext, lang: str) -> None:
    await state.set_state(NewListing.condition)
    await message.answer(t("ask_condition", lang), reply_markup=condition_kb(lang))


def _catalog_photo(data: dict) -> str | None:
    """Official photo of the chosen catalog part, if the catalog has one."""
    for key in ("have_part", "want_part"):
        part = data.get(key)
        if part and part.get("image"):
            return part["image"]
    return None


async def _ask_photos(message: Message, state: FSMContext, lang: str) -> None:
    await state.set_state(NewListing.photos)
    await state.update_data(photo_ids=[], default_photo=None)
    data = await state.get_data()
    has_default = _catalog_photo(data) is not None
    text = t("ask_photos", lang, max=MAX_PHOTOS)
    if has_default:
        text += "\n" + t("ask_photos_catalog", lang)
    await message.answer(text, reply_markup=photos_kb(0, lang, has_default))


@router.message(NewListing.price, PLAIN_TEXT)
async def set_price(message: Message, state: FSMContext, lang: str) -> None:
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) > MAX_PRICE:
        await message.answer(t("bad_price", lang))
        return
    await state.update_data(price_kzt=int(raw))
    await _ask_condition(message, state, lang)


@router.callback_query(NewListing.price, F.data == "price:any")
async def set_price_negotiable(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(price_kzt=None)
    await call.message.edit_text(t("price_set_negotiable", lang))
    await call.answer()
    await _ask_condition(call.message, state, lang)


@router.callback_query(NewListing.condition, F.data.startswith("cond:"))
async def set_condition(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(condition=call.data.split(":")[1])
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _ask_photos(call.message, state, lang)


@router.message(NewListing.photos, F.photo)
async def add_photo(message: Message, state: FSMContext, lang: str) -> None:
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


@router.callback_query(NewListing.photos, F.data == "photos:default")
async def photos_default(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    image = _catalog_photo(data)
    if not image or data.get("photo_ids"):
        await call.answer(t("not_available", lang))
        return
    await state.update_data(default_photo=image)
    try:
        await call.message.answer_photo(image, caption=t("catalog_photo_added", lang))
    except Exception:
        logging.warning("catalog photo preview failed: %s", image)
        await call.message.answer(t("catalog_photo_added", lang))
    await photos_done(call, state, lang)


@router.callback_query(NewListing.photos, F.data == "photos:done")
async def photos_done(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(NewListing.note)
    await call.message.answer(t("ask_note", lang), reply_markup=note_kb(lang))
    await call.answer()


@router.message(NewListing.note, PLAIN_TEXT)
async def set_note(message: Message, state: FSMContext, lang: str) -> None:
    note = message.text.strip()
    if len(note) > MAX_NOTE:
        await message.answer(t("note_too_long", lang, max=MAX_NOTE))
        return
    await state.update_data(note=note)
    await _show_preview(message, state, lang)


@router.callback_query(NewListing.note, F.data == "note:skip")
async def skip_note(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _show_preview(call.message, state, lang)


def _preview(data: dict) -> dict:
    return {
        "type": data["type"],
        "have_part": data.get("have_part"),
        "have_text": data.get("have_text"),
        "want_part": data.get("want_part"),
        "want_text": data.get("want_text"),
        "price_kzt": data.get("price_kzt"),
        "condition": data.get("condition"),
        "note": data.get("note"),
        "photos": data.get("photo_ids") or ([data["default_photo"]] if data.get("default_photo") else []),
    }


async def _show_preview(message: Message, state: FSMContext, lang: str) -> None:
    data = await state.get_data()
    await state.set_state(NewListing.confirm)
    await message.answer(
        t("check_listing", lang) + "\n\n" + format_listing(_preview(data), lang),
        reply_markup=confirm_kb(lang),
    )


@router.callback_query(NewListing.confirm, F.data == "publish")
async def publish(call: CallbackQuery, state: FSMContext, bot: Bot, user: dict, lang: str) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()

    data = await state.get_data()
    photo_urls = []
    photo_ids = data.get("photo_ids", [])
    if photo_ids:
        await call.message.answer(t("uploading_photos", lang))
        try:
            photo_urls = await upload_telegram_photos(bot, photo_ids)
        except Exception:
            logging.exception("photo upload failed")
            await call.message.answer(t("photos_failed_publish", lang))
    if not photo_urls and data.get("default_photo"):
        photo_urls = [data["default_photo"]]

    have_part = data.get("have_part")
    want_part = data.get("want_part")
    listing = await db.create_listing({
        "team_id": user["team_id"],
        "user_tg_id": call.from_user.id,
        "type": data["type"],
        "have_part_id": have_part["id"] if have_part else None,
        "have_text": data.get("have_text"),
        "want_part_id": want_part["id"] if want_part else None,
        "want_text": data.get("want_text"),
        "price_kzt": data.get("price_kzt"),
        "condition": data.get("condition"),
        "note": data.get("note"),
        "city": user["team"]["city"],
        "photos": photo_urls,
    })
    await state.clear()

    shown = format_listing({**listing, "have_part": have_part, "want_part": want_part}, lang)
    await call.message.answer(f"{t('published', lang)}\n\n{shown}", reply_markup=main_menu(lang))
    kb = website_kb(lang, t("btn_view_on_website", lang), listing["id"])
    if kb:
        await call.message.answer(t("live_on_website", lang), reply_markup=kb)
