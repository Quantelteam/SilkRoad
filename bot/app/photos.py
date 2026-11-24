from io import BytesIO

from aiogram import Bot

from app import db


async def upload_telegram_photos(bot: Bot, file_ids: list[str]) -> list[str]:
    """Downloads photos from Telegram and stores them in Supabase."""
    urls = []
    for file_id in file_ids:
        buffer = BytesIO()
        await bot.download(file_id, destination=buffer)
        urls.append(await db.upload_photo(buffer.getvalue()))
    return urls
