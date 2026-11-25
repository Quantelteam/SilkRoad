from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from urllib.parse import urlencode

from app.config import settings
from app.i18n import LANG_NAMES, LANGS, all_translations, t
from app.texts import CONDITIONS, LISTING_TYPES, condition_label, type_label

# Reply-menu buttons, matched in any language (F.text.in_(...)): after a switch
# the user's keyboard may still show the labels of the previous language.
NEW_LISTING = all_translations("btn_new_listing")
MY_LISTINGS = all_translations("btn_my_listings")
WEBSITE = all_translations("btn_website")
LANGUAGE = all_translations("btn_language")


def main_menu(lang: str) -> ReplyKeyboardMarkup:
    rows = [[KeyboardButton(text=t("btn_new_listing", lang))],
            [KeyboardButton(text=t("btn_my_listings", lang))]]
    last = [KeyboardButton(text=t("btn_language", lang))]
    if settings.site_url:
        last.insert(0, KeyboardButton(text=t("btn_website", lang)))
    rows.append(last)
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def language_kb() -> InlineKeyboardMarkup:
    return inline([[(LANG_NAMES[code], f"lang:{code}")] for code in LANGS])


def site_link(listing_id: int | None = None) -> str | None:
    """The website, or one listing on it (the site opens ?listing=<id> in a dialog)."""
    if not settings.site_url:
        return None
    if listing_id is None:
        return settings.site_url + "/listings.html"
    return settings.site_url + "/listings.html?" + urlencode({"listing": listing_id})


def website_kb(lang: str, text: str | None = None,
               listing_id: int | None = None) -> InlineKeyboardMarkup | None:
    url = site_link(listing_id)
    if not url:
        return None
    label = text or t("btn_open_website", lang)
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=label, url=url)]])


def inline(rows: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data=data) for text, data in row]
        for row in rows
    ])


def moderation_kb(request_id: int, lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_approve", lang), f"mod:ok:{request_id}"),
                    (t("btn_reject", lang), f"mod:no:{request_id}")]])


def verify_team_kb(team_id: int, lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_verify_team", lang), f"vt:on:{team_id}")]])


def program_kb() -> InlineKeyboardMarkup:
    return inline([[("FTC", "program:FTC"), ("FLL", "program:FLL")]])


def join_team_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_join_yes", lang), "join:yes")], [(t("btn_join_no", lang), "join:no")]])


def listing_type_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(type_label(kind, lang), f"type:{kind}")] for kind in LISTING_TYPES])


def condition_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(condition_label(key, lang), f"cond:{key}")] for key in CONDITIONS])


def price_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_negotiable", lang), "price:any")]])


def photos_kb(count: int, lang: str, catalog_photo: bool = False) -> InlineKeyboardMarkup:
    label = t("btn_done", lang) if count else t("btn_skip_photos", lang)
    rows = [[(label, "photos:done")]]
    if catalog_photo and not count:
        rows.insert(0, [(t("btn_catalog_photo", lang), "photos:default")])
    return inline(rows)


def note_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_skip", lang), "note:skip")]])


def confirm_kb(lang: str) -> InlineKeyboardMarkup:
    return inline([[(t("btn_publish", lang), "publish")], [(t("btn_cancel", lang), "cancel")]])


def listing_actions_kb(listing_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = inline([[(t("btn_edit", lang), f"edit:{listing_id}"),
                  (t("btn_close", lang), f"close:{listing_id}")]])
    url = site_link(listing_id)
    if url:
        kb.inline_keyboard.append([InlineKeyboardButton(text=t("btn_on_website", lang), url=url)])
    return kb


def edit_menu_kb(listing: dict, lang: str) -> InlineKeyboardMarkup:
    listing_id = listing["id"]
    rows = []
    if listing["type"] == "wanted":
        rows.append([(t("btn_field_wanted_part", lang), f"ef:part:{listing_id}")])
    else:
        rows.append([(t("btn_field_part", lang), f"ef:part:{listing_id}")])
    if listing["type"] == "sell":
        rows.append([(t("btn_field_price", lang), f"ef:price:{listing_id}")])
    if listing["type"] != "wanted":
        rows.append([(t("btn_field_condition", lang), f"ef:cond:{listing_id}")])
    rows.append([(t("btn_field_note", lang), f"ef:note:{listing_id}")])
    rows.append([(t("btn_field_photos", lang), f"ef:photos:{listing_id}")])
    rows.append([(t("btn_back", lang), f"ef:back:{listing_id}")])
    return inline(rows)
