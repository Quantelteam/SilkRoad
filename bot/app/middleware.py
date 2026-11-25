from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app import db


class UserMiddleware(BaseMiddleware):
    """Puts the registered user (with their team) into the handler data."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        user = None
        if tg_user is not None:
            user = await db.get_user(tg_user.id)
            if user and user.get("username") != tg_user.username:
                await db.update_username(tg_user.id, tg_user.username)
                user["username"] = tg_user.username
            # A user with no team (for example a moderator who isn't on any team)
            # counts as not registered: the flows below all need a team.
            # Moderation checks the role in the database, so it still works.
            if user and not user.get("team"):
                user = None
        data["user"] = user
        return await handler(event, data)
