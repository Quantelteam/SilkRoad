"""Long polling, for running the bot on your own computer.

In production the bot runs on Vercel as a webhook (api/telegram.py). Starting
this removes that webhook, so the Vercel bot stops getting messages until
api/setup is called again. Run only one of the two at a time.
"""

import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage

from app.bootstrap import commands, make_bot, make_dispatcher


async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s %(message)s")
    bot = make_bot()
    dp = make_dispatcher(MemoryStorage())
    await bot.set_my_commands(commands())
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("bot started (long polling)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
