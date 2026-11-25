"""Moderators approve or reject teams that are not on the USTEM Connect list.

Messages to a moderator are in that moderator's language (user_prefs); a
moderator who never picked one gets English.
"""

import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message

from app import db
from app.i18n import DEFAULT_LANG, t
from app.keyboards import main_menu, moderation_kb, verify_team_kb

router = Router()

USTEM_TEAMS = "https://connect.ustem.kz/teams"


async def _moderators_with_lang() -> list[tuple[int, str]]:
    ids = sorted(await db.moderator_ids())
    langs = await db.get_langs(ids)
    return [(moderator_id, langs.get(moderator_id, DEFAULT_LANG)) for moderator_id in ids]


async def lang_of(tg_id: int) -> str:
    """The language someone picked, for messages we send them unprompted."""
    return await db.get_lang(tg_id) or DEFAULT_LANG


def request_text(req: dict, lang: str) -> str:
    who = escape(req.get("full_name") or "")
    if req.get("username"):
        who += f" @{escape(req['username'])}"
    return t("mod_request", lang, id=req["id"],
             team=f"{req['program']} #{req['number']} {escape(req['name'])}",
             city=escape(req["city"]), who=who, tg_id=req["tg_id"], url=USTEM_TEAMS)


async def notify_moderators(bot: Bot, req: dict) -> int:
    """Sends the request to every moderator. Returns how many got it."""
    sent = 0
    for moderator_id, lang in await _moderators_with_lang():
        try:
            await bot.send_message(moderator_id, request_text(req, lang),
                                   reply_markup=moderation_kb(req["id"], lang))
            sent += 1
        except Exception:  # a moderator who never started the bot can't be messaged
            logging.warning("could not notify moderator %s about request %s", moderator_id, req["id"])
    return sent


@router.callback_query(F.data.startswith("mod:"))
async def decide(call: CallbackQuery, bot: Bot, lang: str) -> None:
    # The buttons only go to moderators, but anyone can forge a callback: check.
    if call.from_user.id not in await db.moderator_ids():
        await call.answer(t("mods_only", lang), show_alert=True)
        return
    parts = (call.data or "").split(":")
    if len(parts) != 3 or parts[1] not in ("ok", "no") or not parts[2].isdigit():
        await call.answer(t("unknown_action", lang), show_alert=True)
        return
    approve = parts[1] == "ok"
    request_id = int(parts[2])

    req = await db.decide_team_request(request_id, "approved" if approve else "rejected", call.from_user.id)
    if req is None:  # another moderator was faster, or the request is gone
        current = await db.get_team_request(request_id)
        if current is None:
            alert = t("request_not_found", lang)
        elif current["status"] in ("approved", "rejected"):
            alert = t(f"already_{current['status']}", lang)
        else:
            alert = t("already_status", lang, status=current["status"])
        await call.answer(alert, show_alert=True)
        await call.message.edit_reply_markup(reply_markup=None)
        return

    label = f"{req['program']} #{req['number']} {escape(req['name'])}"
    user_lang = await lang_of(req["tg_id"])
    if approve:
        team = await db.create_approved_team(req["program"], req["number"], req["name"], req["city"])
        # A moderator just looked at this team, so it gets the ✓ straight away.
        await db.set_team_checked(team["id"], True, call.from_user.id)
        await db.save_user(req["tg_id"], req.get("username"), req.get("full_name") or "", team["id"])
        await bot.send_message(req["tg_id"], t("team_approved_user", user_lang, team=label),
                               reply_markup=main_menu(user_lang))
    else:
        await bot.send_message(req["tg_id"], t("team_rejected_user", user_lang, team=label, url=USTEM_TEAMS))

    moderator = f"@{escape(call.from_user.username)}" if call.from_user.username else str(call.from_user.id)
    verdict = t("verdict_approved" if approve else "verdict_rejected", lang, moderator=moderator)
    await call.message.edit_text(f"{request_text(req, lang)}\n\n{verdict}")
    await call.answer()


# ---- The verified ✓ ---------------------------------------------------------
# A team gets the ✓ once an admin has checked that its members are who they say.
# Teams without it still post, and the website and bot show them without the mark.

def team_label(team: dict) -> str:
    mark = " ✓" if team.get("checked_at") else ""
    return f"{team['program']} #{team['number']} {escape(team['name'])}{mark}"


async def notify_new_member(bot: Bot, team: dict, tg_user) -> None:
    """Tells admins someone joined a team that has no ✓ yet, with a button to verify it."""
    if team.get("checked_at"):
        return
    who = escape(tg_user.full_name or "")
    if tg_user.username:
        who += f" @{escape(tg_user.username)}"
    for moderator_id, lang in await _moderators_with_lang():
        text = t("new_member", lang, who=who, team=team_label(team), city=escape(team["city"]))
        try:
            await bot.send_message(moderator_id, text, reply_markup=verify_team_kb(team["id"], lang))
        except Exception:
            logging.warning("could not notify moderator %s about team %s", moderator_id, team["id"])


@router.callback_query(F.data.startswith("vt:"))
async def verify_button(call: CallbackQuery, lang: str) -> None:
    if call.from_user.id not in await db.moderator_ids():
        await call.answer(t("admins_only", lang), show_alert=True)
        return
    parts = (call.data or "").split(":")
    if len(parts) != 3 or parts[1] != "on" or not parts[2].isdigit():
        await call.answer(t("unknown_action", lang), show_alert=True)
        return
    team = await db.set_team_checked(int(parts[2]), True, call.from_user.id)
    if team is None:
        await call.answer(t("team_not_found", lang), show_alert=True)
        return
    await call.message.edit_text(f"{call.message.html_text}\n\n{t('verified_line', lang, team=team_label(team))}")
    await call.answer(t("verified_alert", lang))


async def _team_from_args(message: Message, command: CommandObject, lang: str) -> dict | None:
    args = (command.args or "").split()
    if len(args) != 2 or args[0].upper() not in ("FTC", "FLL") or not args[1].lstrip("#").isdigit():
        await message.answer(t("verify_usage", lang, command=command.command))
        return None
    team = await db.find_team(args[0].upper(), int(args[1].lstrip("#")))
    if team is None:
        await message.answer(t("no_such_team", lang))
    return team


@router.message(Command("verify", "unverify"))
async def verify_command(message: Message, command: CommandObject, lang: str) -> None:
    if message.from_user.id not in await db.moderator_ids():
        return  # not an admin: behave like an unknown command
    team = await _team_from_args(message, command, lang)
    if team is None:
        return
    on = command.command == "verify"
    team = await db.set_team_checked(team["id"], on, message.from_user.id)
    key = "verified_line" if on else "verification_removed"
    await message.answer(t(key, lang, team=team_label(team)))
