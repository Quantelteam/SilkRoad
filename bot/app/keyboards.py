from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from app.texts import CONDITION_LABELS, TYPE_LABELS

NEW_LISTING = "➕ New listing"
MY_LISTINGS = "📋 My listings"

main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=NEW_LISTING)], [KeyboardButton(text=MY_LISTINGS)]],
    resize_keyboard=True,
)


def inline(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
        for row in rows
    ])


def program_kb() -> InlineKeyboardMarkup:
    return inline([[("FTC", "program:FTC"), ("FLL", "program:FLL")]])


def join_team_kb() -> InlineKeyboardMarkup:
    return inline([[("Yes, that's my team", "join:yes")], [("No, start over", "join:no")]])


def listing_type_kb() -> InlineKeyboardMarkup:
    return inline([[(TYPE_LABELS[t], f"type:{t}")] for t in ("trade", "sell", "wanted", "give")])


def condition_kb() -> InlineKeyboardMarkup:
    return inline([[(label, f"cond:{key}")] for key, label in CONDITION_LABELS.items()])


def price_kb() -> InlineKeyboardMarkup:
    return inline([[("Negotiable", "price:any")]])


def photos_kb(count: int) -> InlineKeyboardMarkup:
    label = "Done" if count else "Skip photos"
    return inline([[(label, "photos:done")]])


def note_kb() -> InlineKeyboardMarkup:
    return inline([[("Skip", "note:skip")]])


def confirm_kb() -> InlineKeyboardMarkup:
    return inline([[("✅ Publish", "publish")], [("✖️ Cancel", "cancel")]])


def listing_actions_kb(listing_id: int) -> InlineKeyboardMarkup:
    return inline([[("✏️ Edit", f"edit:{listing_id}"), ("✅ Close", f"close:{listing_id}")]])


def edit_menu_kb(listing: dict) -> InlineKeyboardMarkup:
    listing_id = listing["id"]
    rows = []
    if listing["type"] == "wanted":
        rows.append([("Wanted part", f"ef:part:{listing_id}")])
    else:
        rows.append([("Part", f"ef:part:{listing_id}")])
    if listing["type"] == "sell":
        rows.append([("Price", f"ef:price:{listing_id}")])
    if listing["type"] != "wanted":
        rows.append([("Condition", f"ef:cond:{listing_id}")])
    rows.append([("Note", f"ef:note:{listing_id}")])
    rows.append([("Photos", f"ef:photos:{listing_id}")])
    rows.append([("⬅️ Back", f"ef:back:{listing_id}")])
    return inline(rows)
