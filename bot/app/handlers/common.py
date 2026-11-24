from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.keyboards import main_menu

# Commands work inside any step, so this router is included before the flows.
commands = Router()
# Everything the flows did not handle ends up here, so it is included last.
fallback = Router()

HELP = (
    "<b>FTC KZ Parts Exchange</b>\n\n"
    "➕ New listing — post a part you have, need, sell or give away.\n"
    "📋 My listings — edit or close your listings.\n\n"
    "Deals happen in Telegram: teams see your @username on the website and write to you.\n"
    "/cancel — stop what you are doing."
)


@commands.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(HELP, reply_markup=main_menu)


@commands.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu)


@commands.callback_query(F.data == "cancel")
async def cancel_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Cancelled.")
    await call.message.answer("What next?", reply_markup=main_menu)
    await call.answer()


@fallback.message()
async def unknown_message(message: Message, user: dict | None) -> None:
    if not user:
        await message.answer("Send /start to register your team.")
        return
    await message.answer("Use the menu below or /help.", reply_markup=main_menu)


@fallback.callback_query()
async def stale_callback(call: CallbackQuery) -> None:
    await call.answer("That step is over, start again from the menu.", show_alert=True)
