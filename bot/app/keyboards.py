from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from urllib.parse import urlencode

from app.config import settings
from app.texts import CONDITION_LABELS, TYPE_LABELS

NEW_LISTING = "➕ New listing"
MY_LISTINGS = "📋 My listings"
WEBSITE = "🌐 Website"

_menu_rows = [[KeyboardButton(text=NEW_LISTING)], [KeyboardButton(text=MY_LISTINGS)]]
if settings.site_url:
    _menu_rows.append([KeyboardButton(text=WEBSITE)])
main_menu = ReplyKeyboardMarkup(keyboard=_menu_rows, resize_keyboard=True)


def site_link(listing_id: int | None = None) -> str | None:
    """The website, or one listing on it (the site opens ?listing=<id> in a dialog)."""
    if not settings.site_url:
        return None
    if listing_id is None:
        return settings.site_url + "/"
    return settings.site_url + "/?" + urlencode({"listing": listing_id})


def website_kb(text: str = "🌐 Open the website", listing_id: int | None = None) -> InlineKeyboardMarkup | None:
    url = site_link(listing_id)
    if not url:
        return None
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]])


def inline(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
        for row in rows
    ])


def moderation_kb(request_id: int) -> InlineKeyboardMarkup:
    return inline([[("✅ Approve", f"mod:ok:{request_id}"), ("✖️ Reject", f"mod:no:{request_id}")]])


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


def photos_kb(count: int, catalog_photo: bool = False) -> InlineKeyboardMarkup:
    label = "Done" if count else "Skip photos"
    rows = [[(label, "photos:done")]]
    if catalog_photo and not count:
        rows.insert(0, [("🖼 Use the catalog photo", "photos:default")])
    return inline(rows)


def note_kb() -> InlineKeyboardMarkup:
    return inline([[("Skip", "note:skip")]])


def confirm_kb() -> InlineKeyboardMarkup:
    return inline([[("✅ Publish", "publish")], [("✖️ Cancel", "cancel")]])


def listing_actions_kb(listing_id: int) -> InlineKeyboardMarkup:
    kb = inline([[("✏️ Edit", f"edit:{listing_id}"), ("✅ Close", f"close:{listing_id}")]])
    url = site_link(listing_id)
    if url:
        kb.inline_keyboard.append([InlineKeyboardButton(text="🌐 On the website", url=url)])
    return kb


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
