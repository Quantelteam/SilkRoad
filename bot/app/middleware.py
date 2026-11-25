from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from app import db
from app.i18n import DEFAULT_LANG, detect_lang


class UserMiddleware(BaseMiddleware):
    """Puts the registered user (with their team) and their language into the
    handler data: `user`, `lang` and `lang_saved` (False until they pick one)."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        tg_user = data.get("event_from_user")
        user = None
        lang = DEFAULT_LANG
        saved = None
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
            # The language lives in user_prefs, not in FSM data: state.clear()
            # runs all the time and would wipe it.
            saved = await db.get_lang(tg_user.id)
            lang = saved or detect_lang(tg_user.language_code)
        data["user"] = user
        data["lang"] = lang
        data["lang_saved"] = saved is not None
        return await handler(event, data)
