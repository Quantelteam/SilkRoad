from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import db
from app.config import settings
from app.filters import PLAIN_TEXT
from app.keyboards import join_team_kb, main_menu, program_kb
from app.states import Registration

router = Router()

WELCOME = (
    "<b>SilkRoad Exchange</b>\n"
    "Buy. Sell. Exchange.\n\n"
    "Post parts you have or need. Listings show up on the website"
    + (f" ({settings.site_url})" if settings.site_url else "")
    + ", where other teams can find them and write to you in Telegram.\n\n"
    "First, register your team."
)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, user: dict | None) -> None:
    await state.clear()
    if user:
        team = user["team"]
        await message.answer(
            f"You are registered with {team['program']} #{team['number']} "
            f"{team['name']} ({team['city']}).",
            reply_markup=main_menu,
        )
        return
    if not message.from_user.username:
        await message.answer(
            "Your Telegram account has no @username. Other teams need it to contact you.\n"
            "Set one in Telegram → Settings → Username, then send /start again."
        )
        return
    await state.set_state(Registration.program)
    await message.answer(WELCOME, reply_markup=program_kb())


@router.callback_query(Registration.program, F.data.startswith("program:"))
async def pick_program(call: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(program=call.data.split(":")[1])
    await state.set_state(Registration.number)
    await call.message.edit_text("Send your team number (digits only).")
    await call.answer()


@router.message(Registration.number, PLAIN_TEXT)
async def set_number(message: Message, state: FSMContext) -> None:
    raw = message.text.strip().lstrip("#")
    if not raw.isdigit():
        await message.answer("Team number must be digits only, for example 12345.")
        return

    number = int(raw)
    data = await state.get_data()
    existing = await db.find_team(data["program"], number)
    if existing:
        await state.update_data(team_id=existing["id"])
        await state.set_state(Registration.join)
        await message.answer(
            f"{existing['program']} #{existing['number']} {existing['name']} "
            f"({existing['city']}) is already registered. Join it?",
            reply_markup=join_team_kb(),
        )
        return

    await state.update_data(number=number)
    await state.set_state(Registration.name)
    await message.answer("Send your team name.")


@router.callback_query(Registration.join, F.data == "join:yes")
async def join_team(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await db.save_user(
        call.from_user.id,
        call.from_user.username,
        call.from_user.full_name,
        data["team_id"],
    )
    await state.clear()
    await call.message.edit_text("You joined the team.")
    await call.message.answer("Ready. Post your first listing.", reply_markup=main_menu)
    await call.answer()


@router.callback_query(Registration.join, F.data == "join:no")
async def restart_registration(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(Registration.program)
    await call.message.edit_text("Which program is your team in?", reply_markup=program_kb())
    await call.answer()


@router.message(Registration.name, PLAIN_TEXT)
async def set_name(message: Message, state: FSMContext) -> None:
    name = message.text.strip()
    if len(name) < 2 or len(name) > 60:
        await message.answer("Team name must be 2–60 characters.")
        return
    await state.update_data(name=name)
    await state.set_state(Registration.city)
    await message.answer("Send your city, for example Almaty.")


@router.message(Registration.city, PLAIN_TEXT)
async def set_city(message: Message, state: FSMContext) -> None:
    city = message.text.strip()
    if len(city) < 2 or len(city) > 40:
        await message.answer("City must be 2–40 characters.")
        return

    data = await state.get_data()
    team = await db.find_team(data["program"], data["number"])
    if team is None:
        team = await db.create_team(data["program"], data["number"], data["name"], city)
    await db.save_user(
        message.from_user.id, message.from_user.username,
        message.from_user.full_name, team["id"],
    )
    await state.clear()
    await message.answer(
        f"Registered: {team['program']} #{team['number']} {team['name']} ({team['city']}).",
        reply_markup=main_menu,
    )
