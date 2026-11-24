import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import db
from app.config import MAX_PHOTOS, settings
from app.filters import PLAIN_TEXT
from app.handlers.parts_picker import RESOLVERS, ask_part
from app.keyboards import (NEW_LISTING, condition_kb, confirm_kb, listing_type_kb,
                           main_menu, note_kb, photos_kb, price_kb)
from app.photos import upload_telegram_photos
from app.states import NewListing
from app.texts import format_listing

router = Router()

MAX_NOTE = 300
MAX_PRICE = 100_000_000


@router.message(F.text == NEW_LISTING)
async def new_listing(message: Message, state: FSMContext, user: dict | None) -> None:
    if not user:
        await message.answer("Register your team first — send /start.")
        return
    await state.clear()
    await state.set_state(NewListing.type)
    await message.answer("What kind of listing is this?", reply_markup=listing_type_kb())


@router.callback_query(NewListing.type, F.data.startswith("type:"))
async def pick_type(call: CallbackQuery, state: FSMContext) -> None:
    kind = call.data.split(":")[1]
    await state.update_data(type=kind)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    prompt = ("What part do you need?" if kind == "wanted"
              else "What part do you have?")
    await ask_part(call.message, state, prompt, "create_main", NewListing.part)


async def _resolve_main(message: Message, state: FSMContext,
                        part: dict | None, text: str | None) -> None:
    data = await state.get_data()
    kind = data["type"]
    side = "want" if kind == "wanted" else "have"
    await state.update_data(**{f"{side}_part": part, f"{side}_text": text})

    if kind == "trade":
        await ask_part(message, state, "What do you want in return?",
                       "create_want", NewListing.part)
    elif kind == "sell":
        await state.set_state(NewListing.price)
        await message.answer("Price in tenge (digits only), or tap Negotiable.",
                             reply_markup=price_kb())
    elif kind == "give":
        await _ask_condition(message, state)
    else:
        await _ask_photos(message, state)


async def _resolve_want(message: Message, state: FSMContext,
                        part: dict | None, text: str | None) -> None:
    await state.update_data(want_part=part, want_text=text)
    await _ask_condition(message, state)


RESOLVERS["create_main"] = _resolve_main
RESOLVERS["create_want"] = _resolve_want


async def _ask_condition(message: Message, state: FSMContext) -> None:
    await state.set_state(NewListing.condition)
    await message.answer("What condition is the part in?", reply_markup=condition_kb())


async def _ask_photos(message: Message, state: FSMContext) -> None:
    await state.set_state(NewListing.photos)
    await state.update_data(photo_ids=[])
    await message.answer(
        f"Send up to {MAX_PHOTOS} photos of the part, then tap Done.",
        reply_markup=photos_kb(0),
    )


@router.message(NewListing.price, PLAIN_TEXT)
async def set_price(message: Message, state: FSMContext) -> None:
    raw = message.text.strip().replace(" ", "")
    if not raw.isdigit() or int(raw) > MAX_PRICE:
        await message.answer("Send the price as digits, for example 15000.")
        return
    await state.update_data(price_kzt=int(raw))
    await _ask_condition(message, state)


@router.callback_query(NewListing.price, F.data == "price:any")
async def set_price_negotiable(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(price_kzt=None)
    await call.message.edit_text("Price: negotiable")
    await call.answer()
    await _ask_condition(call.message, state)


@router.callback_query(NewListing.condition, F.data.startswith("cond:"))
async def set_condition(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(condition=call.data.split(":")[1])
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _ask_photos(call.message, state)


@router.message(NewListing.photos, F.photo)
async def add_photo(message: Message, state: FSMContext) -> None:
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


@router.callback_query(NewListing.photos, F.data == "photos:done")
async def photos_done(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await state.set_state(NewListing.note)
    await call.message.answer(
        "Add a note if anything matters — quantity, what is broken, pickup details. "
        "Or skip it.",
        reply_markup=note_kb(),
    )
    await call.answer()


@router.message(NewListing.note, PLAIN_TEXT)
async def set_note(message: Message, state: FSMContext) -> None:
    note = message.text.strip()
    if len(note) > MAX_NOTE:
        await message.answer(f"Keep the note under {MAX_NOTE} characters.")
        return
    await state.update_data(note=note)
    await _show_preview(message, state)


@router.callback_query(NewListing.note, F.data == "note:skip")
async def skip_note(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    await _show_preview(call.message, state)


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
        "photos": data.get("photo_ids", []),
    }


async def _show_preview(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(NewListing.confirm)
    await message.answer(
        "Check the listing:\n\n" + format_listing(_preview(data)),
        reply_markup=confirm_kb(),
    )


@router.callback_query(NewListing.confirm, F.data == "publish")
async def publish(call: CallbackQuery, state: FSMContext, bot: Bot, user: dict) -> None:
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()

    data = await state.get_data()
    photo_urls = []
    photo_ids = data.get("photo_ids", [])
    if photo_ids:
        await call.message.answer("Uploading photos…")
        try:
            photo_urls = await upload_telegram_photos(bot, photo_ids)
        except Exception:
            logging.exception("photo upload failed")
            await call.message.answer("Photos could not be uploaded, publishing without them.")

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

    text = f"Published.\n\n{format_listing({**listing, 'have_part': have_part, 'want_part': want_part})}"
    if settings.site_url:
        text += f"\n\n{settings.site_url}"
    await call.message.answer(text, reply_markup=main_menu)
