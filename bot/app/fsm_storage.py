"""Conversation state (which step of a flow a user is on) kept in Supabase.

On Vercel every message may run in a fresh process, so the in-memory storage
used for long polling would forget where a user was. Each key is one row in
bot_fsm; only the bot (service key) can read or write it.
"""

import asyncio
from datetime import datetime, timezone
from typing import Any

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey

from app.db import _client

TABLE = "bot_fsm"


def _key(key: StorageKey) -> str:
    parts = (key.bot_id, key.chat_id, key.user_id, key.thread_id or "",
             getattr(key, "business_connection_id", None) or "", key.destiny)
    return ":".join(str(p) for p in parts)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SupabaseStorage(BaseStorage):
    async def _row(self, key: StorageKey) -> dict | None:
        def run():
            res = _client.table(TABLE).select("state,data").eq("key", _key(key)).limit(1).execute()
            return res.data[0] if res.data else None

        return await asyncio.to_thread(run)

    async def _upsert(self, key: StorageKey, fields: dict) -> None:
        # Upsert writes only the given columns, so state and data don't overwrite each other.
        def run():
            _client.table(TABLE).upsert({"key": _key(key), **fields, "updated_at": _now()}).execute()

        await asyncio.to_thread(run)

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        value = state.state if isinstance(state, State) else state
        await self._upsert(key, {"state": value})

    async def get_state(self, key: StorageKey) -> str | None:
        row = await self._row(key)
        return row["state"] if row else None

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        await self._upsert(key, {"data": data})

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        row = await self._row(key)
        return dict(row["data"] or {}) if row else {}

    async def close(self) -> None:
        pass
