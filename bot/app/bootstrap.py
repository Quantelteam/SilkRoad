"""Builds the bot and its dispatcher. Shared by long polling (app.main, for
running on your own computer) and the Vercel webhook (api/telegram.py)."""

import logging
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import BotCommand, ErrorEvent

from app.config import settings
from app.handlers import build_router
from app.i18n import description, normalize_lang, short_description, t
from app.middleware import UserMiddleware

# Telegram shows the command menu and the bot profile in the user's app
# language: English is the default (no language_code), plus Russian and Kazakh.
PROFILE_LANGS: tuple[tuple[str, str | None], ...] = (("en", None), ("ru", "ru"), ("kk", "kk"))


def commands(lang: str = "en") -> list[BotCommand]:
    items = [
        BotCommand(command="start", description=t("cmd_start", lang)),
        BotCommand(command="help", description=t("cmd_help", lang)),
        BotCommand(command="lang", description=t("cmd_lang", lang)),
        BotCommand(command="cancel", description=t("cmd_cancel", lang)),
    ]
    if settings.site_url:
        items.append(BotCommand(command="site", description=t("cmd_site", lang)))
    return items


async def set_commands(bot: Bot) -> None:
    for lang, code in PROFILE_LANGS:
        await bot.set_my_commands(commands(lang), language_code=code)


async def set_profile(bot: Bot) -> None:
    """Command menu, description and short description in every language."""
    await set_commands(bot)
    for lang, code in PROFILE_LANGS:
        await bot.set_my_description(description(lang), language_code=code)
        await bot.set_my_short_description(short_description(lang), language_code=code)


def make_bot() -> Bot:
    return Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def make_dispatcher(storage: BaseStorage) -> Dispatcher:
    """Call once per process: the routers can only be attached to one dispatcher."""
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(UserMiddleware())
    dp.include_router(build_router())

    @dp.errors()
    async def on_error(event: ErrorEvent, **data: Any) -> bool:
        logging.exception("update failed", exc_info=event.exception)
        message = getattr(event.update, "message", None) or getattr(
            getattr(event.update, "callback_query", None), "message", None)
        if message is not None:
            # UserMiddleware put the language in the data, unless it is what failed.
            await message.answer(t("error_generic", normalize_lang(data.get("lang"))))
        return True

    return dp
