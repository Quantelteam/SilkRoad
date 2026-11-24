import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, ErrorEvent

from app.config import settings
from app.handlers import build_router
from app.middleware import UserMiddleware

COMMANDS = [
    BotCommand(command="start", description="Register or open the menu"),
    BotCommand(command="help", description="How the exchange works"),
    BotCommand(command="cancel", description="Cancel the current step"),
]


async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")

    bot = Bot(settings.bot_token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
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

    await bot.set_my_commands(COMMANDS)
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
