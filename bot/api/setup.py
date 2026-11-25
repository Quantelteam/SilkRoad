"""Vercel serverless function: points Telegram at api/telegram and sets the
command menu. Call it once after each deploy that changes the domain:

    curl -H "X-Setup-Secret: $WEBHOOK_SECRET" https://<bot domain>/api/setup

Add ?check to only read the webhook status. Telegram rate-limits setWebhook,
so use ?check for repeated checks.
"""

import asyncio
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.bootstrap import commands, make_bot  # noqa: E402

SECRET = os.environ.get("WEBHOOK_SECRET", "")

# What Telegram shows on the bot's profile and on its empty chat screen.
BOT_NAME = "Almasu"
SHORT_DESCRIPTION = "Buy. Sell. Exchange. Spare FTC and FLL parts between teams in Kazakhstan."
DESCRIPTION = (
    "Almasu: buy, sell and exchange spare FTC and FLL parts between teams in Kazakhstan.\n\n"
    "Post what your team has or needs here. Every listing also appears on the website, "
    "and deals happen in Telegram private messages."
)


async def _setup(host: str, check_only: bool) -> dict:
    bot = make_bot()
    try:
        if not check_only:
            await bot.set_webhook(
                url=f"https://{host}/api/telegram",
                secret_token=SECRET,
                allowed_updates=["message", "callback_query"],
            )
            await bot.set_my_commands(commands())
            await bot.set_my_name(BOT_NAME)
            await bot.set_my_short_description(SHORT_DESCRIPTION)
            await bot.set_my_description(DESCRIPTION)
        info = await bot.get_webhook_info()
        me = await bot.get_me()
        return {"bot": me.username, "name": me.first_name, "webhook": info.url, "pending": info.pending_update_count,
                "last_error": info.last_error_message}
    finally:
        await bot.session.close()


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        given = self.headers.get("X-Setup-Secret", "")
        if not SECRET or not hmac.compare_digest(given, SECRET):
            return self._reply(403, {"error": "forbidden"})
        host = self.headers.get("x-forwarded-host") or self.headers.get("Host", "")
        check_only = "check" in parse_qs(urlparse(self.path).query, keep_blank_values=True)
        try:
            self._reply(200, asyncio.run(_setup(host, check_only)))
        except Exception as exc:  # e.g. Telegram's "Too Many Requests" on setWebhook
            self._reply(502, {"error": type(exc).__name__, "detail": str(exc)[:300]})

    def _reply(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
