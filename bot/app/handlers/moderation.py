"""Moderators approve or reject teams that are not on the USTEM Connect list."""

import logging
from html import escape

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery

from app import db
from app.keyboards import main_menu, moderation_kb

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
