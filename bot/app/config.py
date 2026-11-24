import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    supabase_url: str
    supabase_service_key: str
    site_url: str


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set — copy .env.example to .env and fill it in")
    return value


settings = Settings(
    bot_token=_required("BOT_TOKEN"),
    supabase_url=_required("SUPABASE_URL"),
    supabase_service_key=_required("SUPABASE_SERVICE_KEY"),
    site_url=os.getenv("SITE_URL", "").strip(),
)

PHOTO_BUCKET = "listings"
MAX_PHOTOS = 3
