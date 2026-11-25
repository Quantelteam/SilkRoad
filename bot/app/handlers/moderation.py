"""Moderators approve or reject teams that are not on the USTEM Connect list."""

import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, Message

from app import db
from app.keyboards import main_menu, moderation_kb, verify_team_kb

router = Router()

USTEM_TEAMS = "https://connect.ustem.kz/teams"


def request_text(req: dict) -> str:
    who = escape(req.get("full_name") or "")
    if req.get("username"):
        who += f" @{escape(req['username'])}"
    return (
        f"<b>Team request #{req['id']}</b>\n"
        f"{req['program']} #{req['number']} {escape(req['name'])} ({escape(req['city'])})\n"
        f"From: {who} (id {req['tg_id']})\n\n"
        f"Not on the USTEM Connect list. Check it: {USTEM_TEAMS}"
    )


async def notify_moderators(bot: Bot, req: dict) -> int:
    """Sends the request to every moderator. Returns how many got it."""
    sent = 0
    for moderator_id in await db.moderator_ids():
        try:
            await bot.send_message(moderator_id, request_text(req), reply_markup=moderation_kb(req["id"]))
            sent += 1
        except Exception:  # a moderator who never started the bot can't be messaged
            logging.warning("could not notify moderator %s about request %s", moderator_id, req["id"])
    return sent


@router.callback_query(F.data.startswith("mod:"))
async def decide(call: CallbackQuery, bot: Bot) -> None:
    # The buttons only go to moderators, but anyone can forge a callback: check.
    if call.from_user.id not in await db.moderator_ids():
        await call.answer("Only moderators can do this.", show_alert=True)
        return
    parts = (call.data or "").split(":")
    if len(parts) != 3 or parts[1] not in ("ok", "no") or not parts[2].isdigit():
        await call.answer("Unknown action.", show_alert=True)
        return
    approve = parts[1] == "ok"
    request_id = int(parts[2])

    req = await db.decide_team_request(request_id, "approved" if approve else "rejected", call.from_user.id)
    if req is None:  # another moderator was faster, or the request is gone
        current = await db.get_team_request(request_id)
        await call.answer(f"Already {current['status']}." if current else "Request not found.", show_alert=True)
        await call.message.edit_reply_markup(reply_markup=None)
        return

    label = f"{req['program']} #{req['number']} {escape(req['name'])}"
    if approve:
        team = await db.create_approved_team(req["program"], req["number"], req["name"], req["city"])
        # A moderator just looked at this team, so it gets the ✓ straight away.
        await db.set_team_checked(team["id"], True, call.from_user.id)
        await db.save_user(req["tg_id"], req.get("username"), req.get("full_name") or "", team["id"])
        await bot.send_message(req["tg_id"], f"✅ Your team {label} was approved. You can post listings now.",
                               reply_markup=main_menu)
    else:
        await bot.send_message(
            req["tg_id"],
            f"A moderator didn't approve {label}. Check your team number on {USTEM_TEAMS} "
            "and send /start to try again.",
        )

    moderator = f"@{escape(call.from_user.username)}" if call.from_user.username else str(call.from_user.id)
    verdict = "✅ Approved" if approve else "✖️ Rejected"
    await call.message.edit_text(f"{request_text(req)}\n\n{verdict} by {moderator}")
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
    text = (f"<b>New member, team not verified</b>\n{who} joined {team_label(team)} "
            f"({escape(team['city'])}).\n\nIf you know they're on this team, verify it.")
    for moderator_id in await db.moderator_ids():
        try:
            await bot.send_message(moderator_id, text, reply_markup=verify_team_kb(team["id"]))
        except Exception:
            logging.warning("could not notify moderator %s about team %s", moderator_id, team["id"])


@router.callback_query(F.data.startswith("vt:"))
async def verify_button(call: CallbackQuery) -> None:
    if call.from_user.id not in await db.moderator_ids():
        await call.answer("Only admins can do this.", show_alert=True)
        return
    parts = (call.data or "").split(":")
    if len(parts) != 3 or parts[1] != "on" or not parts[2].isdigit():
        await call.answer("Unknown action.", show_alert=True)
        return
    team = await db.set_team_checked(int(parts[2]), True, call.from_user.id)
    if team is None:
        await call.answer("Team not found.", show_alert=True)
        return
    await call.message.edit_text(f"{call.message.html_text}\n\n✓ Verified: {team_label(team)}")
    await call.answer("Verified")


async def _team_from_args(message: Message, command: CommandObject) -> dict | None:
    args = (command.args or "").split()
    if len(args) != 2 or args[0].upper() not in ("FTC", "FLL") or not args[1].lstrip("#").isdigit():
        await message.answer(f"Usage: /{command.command} FTC 24881")
        return None
    team = await db.find_team(args[0].upper(), int(args[1].lstrip("#")))
    if team is None:
        await message.answer("No such team in the database.")
    return team


@router.message(Command("verify", "unverify"))
async def verify_command(message: Message, command: CommandObject) -> None:
    if message.from_user.id not in await db.moderator_ids():
        return  # not an admin: behave like an unknown command
    team = await _team_from_args(message, command)
    if team is None:
        return
    on = command.command == "verify"
    team = await db.set_team_checked(team["id"], on, message.from_user.id)
    await message.answer(f"{'✓ Verified' if on else 'Verification removed'}: {team_label(team)}")
