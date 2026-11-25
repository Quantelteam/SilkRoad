from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.i18n import LANG_PICKER_TEXT, t
from app.keyboards import LANGUAGE, WEBSITE, language_kb, main_menu, website_kb

# Commands work inside any step, so this router is included before the flows.
commands = Router()
# Everything the flows did not handle ends up here, so it is included last.
fallback = Router()


def help_text(lang: str) -> str:
    site_line = t("help_site_line", lang, url=settings.site_url) if settings.site_url else ""
    return t("help", lang, site_line=site_line)


@commands.message(Command("help"))
async def help_command(message: Message, lang: str) -> None:
    await message.answer(help_text(lang), reply_markup=main_menu(lang))


@commands.message(Command("lang"))
@commands.message(F.text.in_(LANGUAGE))
async def language_command(message: Message) -> None:
    # The choice is handled in handlers/registration.py (callback lang:<code>).
    await message.answer(LANG_PICKER_TEXT, reply_markup=language_kb())


@commands.message(Command("site"))
@commands.message(F.text.in_(WEBSITE))
async def website(message: Message, lang: str) -> None:
    kb = website_kb(lang)
    if kb is None:
        await message.answer(t("site_offline", lang), reply_markup=main_menu(lang))
        return
    await message.answer(t("site_intro", lang), reply_markup=kb)


@commands.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext, lang: str) -> None:
    await state.clear()
    await message.answer(t("cancelled", lang), reply_markup=main_menu(lang))


@commands.callback_query(F.data == "cancel")
async def cancel_callback(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await call.message.edit_text(t("cancelled", lang))
    await call.message.answer(t("what_next", lang), reply_markup=main_menu(lang))
    await call.answer()


@fallback.message()
async def unknown_message(message: Message, user: dict | None, lang: str) -> None:
    if not user:
        await message.answer(t("send_start", lang))
        return
    await message.answer(t("use_menu", lang), reply_markup=main_menu(lang))


@fallback.callback_query()
async def stale_callback(call: CallbackQuery, lang: str) -> None:
    await call.answer(t("stale_step", lang), show_alert=True)
