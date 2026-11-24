from aiogram import Router

from app.handlers import common, listing_create, moderation, my_listings, parts_picker, registration


def build_router() -> Router:
    """Commands first so they work inside any step, catch-all last."""
    router = Router()
    router.include_routers(
        moderation.router,
        registration.router,
        common.commands,
        listing_create.router,
        my_listings.router,
        parts_picker.router,
        common.fallback,
    )
    return router
