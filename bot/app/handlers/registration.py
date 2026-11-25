from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from app import db
from app.config import settings
from app.filters import PLAIN_TEXT
from app.i18n import LANG_NAMES, LANG_PICKER_TEXT, LANGS, t
from app.keyboards import join_team_kb, language_kb, main_menu, program_kb
from app.handlers.moderation import USTEM_TEAMS, notify_moderators, notify_new_member
from app.states import Registration

router = Router()


def welcome(lang: str) -> str:
    site = f" ({settings.site_url})" if settings.site_url else ""
    return t("welcome", lang, site=site)


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, user: dict | None,
                lang: str, lang_saved: bool) -> None:
    await state.clear()
    if not lang_saved:
        # First contact: ask for the language, then carry on in pick_language.
        await message.answer(LANG_PICKER_TEXT, reply_markup=language_kb())
        return
    await _start_flow(message, state, user, message.from_user, lang)


async def _start_flow(message: Message, state: FSMContext, user: dict | None,
                      tg_user: User, lang: str) -> None:
    """What /start does once the language is known. `message` is where to answer,
    `tg_user` is who it is for (they differ when coming from a button)."""
    await state.clear()
    if user:
        team = user["team"]
        await message.answer(
            t("already_registered", lang,
              team=f"{team['program']} #{team['number']} {escape(team['name'])} ({escape(team['city'])})"),
            reply_markup=main_menu(lang),
        )
        return
    pending = await db.pending_request_for_user(tg_user.id)
    if pending:
        await message.answer(t("pending_request", lang,
                               team=f"{pending['program']} #{pending['number']} {escape(pending['name'])}"))
        return
    if not tg_user.username:
        await message.answer(t("no_username", lang))
        return
    await state.set_state(Registration.program)
    await message.answer(welcome(lang), reply_markup=program_kb())


@router.callback_query(F.data.startswith("lang:"))
async def pick_language(call: CallbackQuery, state: FSMContext, user: dict | None) -> None:
    """From the first /start, /lang or the menu button. Works in any step."""
    lang = (call.data or "").split(":", 1)[1]
    if lang not in LANGS:
        await call.answer()
        return
    await db.set_lang(call.from_user.id, lang)
    await call.message.edit_text(t("lang_set", lang, name=LANG_NAMES[lang]))
    await call.answer()
    if user:
        # Registered: just switch the menu; whatever step they were on stays.
        await call.message.answer(t("menu_hint", lang), reply_markup=main_menu(lang))
        return
    if await state.get_state() is not None:
        return  # /lang in the middle of registration: carry on with that step
    await _start_flow(call.message, state, user, call.from_user, lang)


@router.callback_query(Registration.program, F.data.startswith("program:"))
async def pick_program(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.update_data(program=call.data.split(":")[1])
    await state.set_state(Registration.number)
    await call.message.edit_text(t("ask_team_number", lang))
    await call.answer()


@router.message(Registration.number, PLAIN_TEXT)
async def set_number(message: Message, state: FSMContext, lang: str) -> None:
    raw = message.text.strip().lstrip("#")
    if not raw.isdigit():
        await message.answer(t("bad_team_number", lang))
        return

    number = int(raw)
    data = await state.get_data()
    existing = await db.find_team(data["program"], number)
    if existing:
        await state.update_data(team_id=existing["id"])
        await state.set_state(Registration.join)
        await message.answer(
            t("found_team", lang, team=f"{existing['program']} #{existing['number']} "
                                       f"{escape(existing['name'])} ({escape(existing['city'])})"),
            reply_markup=join_team_kb(lang),
        )
        return

    waiting = await db.pending_request_for_team(data["program"], number)
    if waiting:
        await state.clear()
        await message.answer(t("team_waiting", lang, team=f"{data['program']} #{number}"))
        return

    await state.update_data(number=number)
    await state.set_state(Registration.name)
    await message.answer(t("not_on_ustem", lang, team=f"{data['program']} #{number}", url=USTEM_TEAMS))


@router.callback_query(Registration.join, F.data == "join:yes")
async def join_team(call: CallbackQuery, state: FSMContext, bot: Bot, lang: str) -> None:
    data = await state.get_data()
    await db.save_user(
        call.from_user.id,
        call.from_user.username,
        call.from_user.full_name,
        data["team_id"],
    )
    await state.clear()
    await call.message.edit_text(t("joined_team", lang))
    await call.message.answer(t("ready_first_listing", lang), reply_markup=main_menu(lang))
    await call.answer()
    team = await db.get_team(data["team_id"])
    if team:
        await notify_new_member(bot, team, call.from_user)


@router.callback_query(Registration.join, F.data == "join:no")
async def restart_registration(call: CallbackQuery, state: FSMContext, lang: str) -> None:
    await state.clear()
    await state.set_state(Registration.program)
    await call.message.edit_text(t("which_program", lang), reply_markup=program_kb())
    await call.answer()


@router.message(Registration.name, PLAIN_TEXT)
async def set_name(message: Message, state: FSMContext, lang: str) -> None:
    name = message.text.strip()
    if len(name) < 2 or len(name) > 60:
        await message.answer(t("bad_team_name", lang))
        return
    await state.update_data(name=name)
    await state.set_state(Registration.city)
    await message.answer(t("ask_city", lang))


@router.message(Registration.city, PLAIN_TEXT)
async def set_city(message: Message, state: FSMContext, bot: Bot, lang: str) -> None:
    city = message.text.strip()
    if len(city) < 2 or len(city) > 40:
        await message.answer(t("bad_city", lang))
        return

    data = await state.get_data()
    await state.clear()
    # The team may have been added while this user was typing.
    team = await db.find_team(data["program"], data["number"])
    if team:
        await db.save_user(message.from_user.id, message.from_user.username,
                           message.from_user.full_name, team["id"])
        await message.answer(t("registered", lang,
                               team=f"{team['program']} #{team['number']} {escape(team['name'])}"),
                             reply_markup=main_menu(lang))
        await notify_new_member(bot, team, message.from_user)
        return

    req = await db.create_team_request({
        "program": data["program"], "number": data["number"], "name": data["name"], "city": city,
        "tg_id": message.from_user.id, "username": message.from_user.username,
        "full_name": message.from_user.full_name,
    })
    if req is None:
        await message.answer(t("request_exists", lang))
        return
    sent = await notify_moderators(bot, req)
    if sent:
        await message.answer(t("request_sent", lang,
                               team=f"{req['program']} #{req['number']} {escape(req['name'])}",
                               city=escape(city)))
    else:
        await message.answer(t("request_saved_no_mods", lang))
