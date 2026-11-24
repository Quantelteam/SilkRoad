import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import db
from app.config import MAX_PHOTOS
from app.filters import PLAIN_TEXT
from app.handlers.parts_picker import RESOLVERS, ask_part
from app.keyboards import (MY_LISTINGS, condition_kb, edit_menu_kb, listing_actions_kb,
                           main_menu, note_kb, photos_kb, price_kb)
from app.photos import upload_telegram_photos
from app.states import EditListing
from app.texts import format_listing

router = Router()

MAX_NOTE = 300
MAX_PRICE = 100_000_000


@router.message(F.text == MY_LISTINGS)
async def my_listings(message: Message, state: FSMContext, user: dict | None) -> None:
    if not user:
        await message.answer("Register your team first — send /start.")
        return
    await state.clear()
    listings = await db.user_listings(message.from_user.id)
    if not listings:
        await message.answer("You have no active listings.", reply_markup=main_menu)
        return
    for listing in listings:
        await message.answer(format_listing(listing),
                             reply_markup=listing_actions_kb(listing["id"]))


async def _send_listing(message: Message, listing_id: int, tg_id: int) -> None:
    listing = await db.get_listing(listing_id, tg_id)
    if listing is None:
        await message.answer("That listing is gone.")
        return
    await message.answer(format_listing(listing),
                         reply_markup=listing_actions_kb(listing_id))


# --- close -----------------------------------------------------------------

@router.callback_query(F.data.startswith("close:"))
async def close_listing(call: CallbackQuery) -> None:
    listing_id = int(call.data.split(":")[1])
    listing = await db.update_listing(listing_id, call.from_user.id, {"status": "closed"})
    if listing is None:
        await call.answer("That listing is not yours.", show_alert=True)
        return
    await call.message.edit_text(f"Listing #{listing_id} closed. It is off the website now.")
    await call.answer()


# --- edit ------------------------------------------------------------------

@router.callback_query(F.data.startswith("edit:"))
async def edit_listing(call: CallbackQuery, state: FSMContext) -> None:
    listing_id = int(call.data.split(":")[1])
    listing = await db.get_listing(listing_id, call.from_user.id)
    if listing is None:
        await call.answer("That listing is not yours.", show_alert=True)
        return
    await state.clear()
    await state.set_state(EditListing.menu)
    await state.update_data(listing_id=listing_id, type=listing["type"],
                            tg_id=call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=edit_menu_kb(listing))
    await call.answer()


@router.callback_query(EditListing.menu, F.data.startswith("ef:"))
async def edit_field(call: CallbackQuery, state: FSMContext) -> None:
    _, field, raw_id = call.data.split(":")
    listing_id = int(raw_id)
    data = await state.get_data()
    kind = data.get("type")

    if field == "back":
        await state.clear()
        await call.message.edit_reply_markup(reply_markup=listing_actions_kb(listing_id))
        await call.answer()
        return

    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()

    if field == "part":
        prompt = ("Which part do you need?" if kind == "wanted"
                  else "Which part do you have?")
        await ask_part(call.message, state, prompt, "edit_part", EditListing.part)
    elif field == "price":
        await state.set_state(EditListing.price)
        await call.message.answer("New price in tenge, or tap Negotiable.",
                                  reply_markup=price_kb())
    elif field == "cond":
        await state.set_state(EditListing.condition)
        await call.message.answer("New condition:", reply_markup=condition_kb())
    elif field == "note":
        await state.set_state(EditListing.note)
        await call.message.answer("Send the new note.", reply_markup=note_kb())
    elif field == "photos":
        await state.set_state(EditListing.photos)
        await state.update_data(photo_ids=[])
        await call.message.answer(
            f"Send up to {MAX_PHOTOS} new photos — they replace the current ones.",
            reply_markup=photos_kb(0),
        )


async def _apply(message: Message, state: FSMContext, fields: dict) -> None:
    data = await state.get_data()
    listing_id, tg_id = data["listing_id"], data["tg_id"]
    updated = await db.update_listing(listing_id, tg_id, fields)
    await state.clear()
    if updated is None:
        await message.answer("That listing is gone.")
        return
    await _send_listing(message, listing_id, tg_id)


async def _resolve_edit_part(message: Message, state: FSMContext,
                             part: dict | None, text: str | None) -> None:
    data = await state.get_data()
    side = "want" if data.get("type") == "wanted" else "have"
    await _apply(message, state, {
        f"{side}_part_id": part["id"] if part else None,
        f"{side}_text": text,
    })


RESOLVERS["edit_part"] = _resolve_edit_part


@router.message(EditListing.price, PLAIN_TEXT)
async def edit_price(message: Message, state: FSMContext) -> None:
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) > MAX_PRICE:
        await message.answer("Send the price as digits, for example 15000.")
        return
    await _apply(message, state, {"price_kzt": int(raw)})


@router.callback_query(EditListing.price, F.data == "price:any")
async def edit_price_negotiable(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_text("Price: negotiable")
    await call.answer()
    await _apply(call.message, state, {"price_kzt": None})


@router.callback_query(EditListing.condition, F.data.startswith("cond:"))
async def edit_condition(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _apply(call.message, state, {"condition": call.data.split(":")[1]})


@router.message(EditListing.note, PLAIN_TEXT)
async def edit_note(message: Message, state: FSMContext) -> None:
    note = message.text.strip()
    if len(note) > MAX_NOTE:
        await message.answer(f"Keep the note under {MAX_NOTE} characters.")
        return
    await _apply(message, state, {"note": note})


@router.callback_query(EditListing.note, F.data == "note:skip")
async def clear_note(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _apply(call.message, state, {"note": None})


@router.message(EditListing.photos, F.photo)
async def edit_add_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    if len(photo_ids) >= MAX_PHOTOS:
        await message.answer(f"{MAX_PHOTOS} photos is the limit. Tap Done.",
                             reply_markup=photos_kb(len(photo_ids)))
        return
    photo_ids.append(message.photo[-1].file_id)
    await state.update_data(photo_ids=photo_ids)
    await message.answer(f"Photo {len(photo_ids)}/{MAX_PHOTOS} added.",
                         reply_markup=photos_kb(len(photo_ids)))


@router.callback_query(EditListing.photos, F.data == "photos:done")
async def edit_photos_done(call: CallbackQuery, state: FSMContext, bot: Bot) -> None:
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
            await call.message.answer("Photos could not be uploaded, nothing changed.")
            await state.clear()
            return
    await _apply(call.message, state, {"photos": urls})
