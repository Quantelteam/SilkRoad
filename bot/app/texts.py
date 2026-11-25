"""Labels and listing rendering."""

from html import escape

TYPE_LABELS = {
    "trade": "🔄 Trade",
    "sell": "💰 For sale",
    "wanted": "🔎 Wanted",
    "give": "🎁 Give away",
}

CONDITION_LABELS = {
    "new": "New",
    "used": "Used — working",
    "broken": "Broken — for parts",
}

MAIN_MENU_HINT = "Use the menu below."


def part_label(part: dict) -> str:
    brand = part.get("brand")
    return f"{brand} {part['name']}" if brand else part["name"]


def price_label(price: int | None) -> str:
    if price is None:
        return "Negotiable"
    return f"{price:,}".replace(",", " ") + " ₸"


def _side(part: dict | None, text: str | None) -> str | None:
    if part:
        return part_label(part)
    return text


def format_listing(listing: dict, team: dict | None = None, username: str | None = None) -> str:
    kind = listing["type"]
    header = f"<b>{TYPE_LABELS[kind]}</b>"
    if listing.get("id"):
        header += f" · #{listing['id']}"
    lines = [header]

    have = _side(listing.get("have_part"), listing.get("have_text"))
    want = _side(listing.get("want_part"), listing.get("want_text"))

    if kind == "wanted":
        lines.append(f"Looking for: <b>{escape(want or '-')}</b>")
    else:
        lines.append(f"Have: <b>{escape(have or '-')}</b>")
        if kind == "sell":
            lines.append(f"Price: {price_label(listing.get('price_kzt'))}")
        elif kind == "trade":
            lines.append(f"Want: {escape(want or 'any offer')}")

    if listing.get("condition"):
        lines.append(f"Condition: {CONDITION_LABELS[listing['condition']]}")
    if listing.get("note"):
        lines.append(f"Note: {escape(listing['note'])}")

    if team:
        mark = " ✓" if team.get("checked_at") else ""
        lines.append(f"Team: {team['program']} #{team['number']} {escape(team['name'])}{mark} · {escape(team['city'])}")
    elif listing.get("city"):
        lines.append(f"City: {escape(listing['city'])}")
    if username:
        lines.append(f"Contact: @{username}")

    photos = listing.get("photos") or []
    if photos:
        lines.append(f"Photos: {len(photos)}")

    return "\n".join(lines)
