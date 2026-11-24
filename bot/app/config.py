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
    admin_ids: frozenset[int]


def _site_url() -> str:
    value = os.getenv("SITE_URL", "").strip().rstrip("/")
    if value and not value.startswith("https://"):
        raise RuntimeError("SITE_URL must start with https://, for example https://silkroad.example")
    return value


def _admin_ids() -> frozenset[int]:
    """Telegram user IDs of moderators, comma separated, for example 12345,67890."""
    raw = os.getenv("ADMIN_IDS", "")
    ids = set()
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if not part.isdigit():
            raise RuntimeError(f"ADMIN_IDS must be numeric Telegram IDs, got {part!r}")
        ids.add(int(part))
    return frozenset(ids)


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is not set — copy .env.example to .env and fill it in")
    return value


settings = Settings(
    bot_token=_required("BOT_TOKEN"),
    supabase_url=_required("SUPABASE_URL"),
    supabase_service_key=_required("SUPABASE_SERVICE_KEY"),
    site_url=_site_url(),
    admin_ids=_admin_ids(),
)

PHOTO_BUCKET = "listings"
MAX_PHOTOS = 3
