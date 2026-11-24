"""Thin async wrapper around Supabase. The bot writes, the website reads."""

import asyncio
import re
import uuid
from datetime import datetime, timezone

from supabase import create_client

from app.config import PHOTO_BUCKET, settings

_client = create_client(settings.supabase_url, settings.supabase_service_key)

# PostgREST `or` filters are comma/parenthesis separated, so those characters
# cannot be part of a search term.
_UNSAFE = re.compile(r"[,()%*\\]")


# --- teams and users -------------------------------------------------------

async def find_team(program: str, number: int) -> dict | None:
    def run():
        res = (_client.table("teams").select("*")
               .eq("program", program).eq("number", number).limit(1).execute())
        return res.data[0] if res.data else None

    return await asyncio.to_thread(run)


async def create_team(program: str, number: int, name: str, city: str) -> dict:
    def run():
        res = (_client.table("teams")
               .insert({"program": program, "number": number, "name": name, "city": city})
               .execute())
        return res.data[0]

    return await asyncio.to_thread(run)


async def get_user(tg_id: int) -> dict | None:
    def run():
        res = (_client.table("users").select("*, team:teams(*)")
               .eq("tg_id", tg_id).limit(1).execute())
        return res.data[0] if res.data else None

    return await asyncio.to_thread(run)


async def save_user(tg_id: int, username: str | None, full_name: str, team_id: int) -> dict:
    def run():
        res = (_client.table("users")
               .upsert({"tg_id": tg_id, "username": username,
                        "full_name": full_name, "team_id": team_id})
               .execute())
        return res.data[0]

    return await asyncio.to_thread(run)


async def update_username(tg_id: int, username: str | None) -> None:
    def run():
        _client.table("users").update({"username": username}).eq("tg_id", tg_id).execute()

    await asyncio.to_thread(run)


# --- parts catalog ---------------------------------------------------------

async def search_parts(query: str, limit: int = 10) -> list[dict]:
    term = _UNSAFE.sub(" ", query).strip()
    if not term:
        return []

    def run():
        res = (_client.table("parts").select("*")
               .or_(f"name.ilike.%{term}%,sku.ilike.%{term}%,brand.ilike.%{term}%")
               .order("name").limit(limit).execute())
        return res.data

    return await asyncio.to_thread(run)


async def list_categories() -> list[str]:
    def run():
        res = _client.table("parts").select("category").execute()
        return sorted({row["category"] for row in res.data})

    return await asyncio.to_thread(run)


async def parts_in_category(category: str, limit: int = 40) -> list[dict]:
    def run():
        res = (_client.table("parts").select("*")
               .eq("category", category).order("name").limit(limit).execute())
        return res.data

    return await asyncio.to_thread(run)


async def get_part(part_id: int) -> dict | None:
    def run():
        res = _client.table("parts").select("*").eq("id", part_id).limit(1).execute()
        return res.data[0] if res.data else None

    return await asyncio.to_thread(run)


# --- listings --------------------------------------------------------------

_LISTING_SELECT = "*, have_part:parts!listings_have_part_id_fkey(*), want_part:parts!listings_want_part_id_fkey(*)"


async def create_listing(data: dict) -> dict:
    def run():
        res = _client.table("listings").insert(data).execute()
        return res.data[0]

    return await asyncio.to_thread(run)


async def user_listings(tg_id: int, status: str = "active") -> list[dict]:
    def run():
        res = (_client.table("listings").select(_LISTING_SELECT)
               .eq("user_tg_id", tg_id).eq("status", status)
               .order("created_at", desc=True).execute())
        return res.data

    return await asyncio.to_thread(run)


async def get_listing(listing_id: int, tg_id: int | None = None) -> dict | None:
    def run():
        query = _client.table("listings").select(_LISTING_SELECT).eq("id", listing_id)
        if tg_id is not None:
            query = query.eq("user_tg_id", tg_id)
        res = query.limit(1).execute()
        return res.data[0] if res.data else None

    return await asyncio.to_thread(run)


async def update_listing(listing_id: int, tg_id: int, fields: dict) -> dict | None:
    now = datetime.now(timezone.utc).isoformat()

    def run():
        res = (_client.table("listings").update({**fields, "updated_at": now})
               .eq("id", listing_id).eq("user_tg_id", tg_id).execute())
        return res.data[0] if res.data else None

    return await asyncio.to_thread(run)


# --- photos ----------------------------------------------------------------

async def upload_photo(image: bytes) -> str:
    path = f"{uuid.uuid4().hex}.jpg"

    def run():
        storage = _client.storage.from_(PHOTO_BUCKET)
        storage.upload(path, image, {"content-type": "image/jpeg"})
        return storage.get_public_url(path)

    return await asyncio.to_thread(run)
