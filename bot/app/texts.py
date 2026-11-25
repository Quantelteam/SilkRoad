"""Labels and listing rendering."""

from html import escape

from app.i18n import t

LISTING_TYPES = ("trade", "sell", "wanted", "give")
CONDITIONS = ("new", "used", "broken")


def type_label(kind: str, lang: str) -> str:
    return t(f"type_{kind}", lang)


def condition_label(condition: str, lang: str) -> str:
    return t(f"cond_{condition}", lang)


def part_label(part: dict) -> str:
    brand = part.get("brand")
    return f"{brand} {part['name']}" if brand else part["name"]


def price_label(price: int | None, lang: str) -> str:
    if price is None:
        return t("price_negotiable", lang)
    return f"{price:,}".replace(",", " ") + " ₸"


def _side(part: dict | None, text: str | None) -> str | None:
    if part:
        return part_label(part)
    return text


def format_listing(listing: dict, lang: str, team: dict | None = None, username: str | None = None) -> str:
    kind = listing["type"]
    header = f"<b>{type_label(kind, lang)}</b>"
    if listing.get("id"):
        header += f" · #{listing['id']}"
    lines = [header]

    have = _side(listing.get("have_part"), listing.get("have_text"))
    want = _side(listing.get("want_part"), listing.get("want_text"))

    if kind == "wanted":
        lines.append(t("lst_looking_for", lang, value=escape(want or '-')))
    else:
        lines.append(t("lst_have", lang, value=escape(have or '-')))
        if kind == "sell":
            lines.append(t("lst_price", lang, value=price_label(listing.get('price_kzt'), lang)))
        elif kind == "trade":
            lines.append(t("lst_want", lang, value=escape(want or t("lst_any_offer", lang))))

    if listing.get("condition"):
        lines.append(t("lst_condition", lang, value=condition_label(listing['condition'], lang)))
    if listing.get("note"):
        lines.append(t("lst_note", lang, value=escape(listing['note'])))

    if team:
        mark = " ✓" if team.get("checked_at") else ""
        lines.append(t("lst_team", lang, value=f"{team['program']} #{team['number']} "
                                               f"{escape(team['name'])}{mark} · {escape(team['city'])}"))
    elif listing.get("city"):
        lines.append(t("lst_city", lang, value=escape(listing['city'])))
    if username:
        lines.append(t("lst_contact", lang, value=username))

    photos = listing.get("photos") or []
    if photos:
        lines.append(t("lst_photos", lang, count=len(photos)))

    return "\n".join(lines)
