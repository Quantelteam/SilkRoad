"""Builds the bot and its dispatcher. Shared by long polling (app.main, for
running on your own computer) and the Vercel webhook (api/telegram.py)."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import BotCommand, ErrorEvent

from app.config import settings
from app.handlers import build_router
from app.middleware import UserMiddleware


def commands() -> list[BotCommand]:
    items = [
        BotCommand(command="start", description="Register or open the menu"),
        BotCommand(command="help", description="How the exchange works"),
        BotCommand(command="cancel", description="Cancel the current step"),
    ]
    if settings.site_url:
        items.append(BotCommand(command="site", description="Open the website"))
    return items


def make_bot() -> Bot:
    return Bot(settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def make_dispatcher(storage: BaseStorage) -> Dispatcher:
    """Call once per process: the routers can only be attached to one dispatcher."""
    dp = Dispatcher(storage=storage)
    dp.update.outer_middleware(UserMiddleware())
    dp.include_router(build_router())

    @dp.errors()
    async def on_error(event: ErrorEvent) -> bool:
        logging.exception("update failed", exc_info=event.exception)
        message = getattr(event.update, "message", None) or getattr(
            getattr(event.update, "callback_query", None), "message", None)
        if message is not None:
            await message.answer("Something broke on our side. Try again or send /cancel.")
        return True

    return dp
