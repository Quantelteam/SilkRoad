"""Vercel serverless function: points Telegram at api/telegram and sets the
command menu. Call it once after each deploy that changes the domain:

    curl -H "X-Setup-Secret: $WEBHOOK_SECRET" https://<bot domain>/api/setup
"""

import asyncio
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.bootstrap import commands, make_bot  # noqa: E402

SECRET = os.environ.get("WEBHOOK_SECRET", "")


async def _setup(host: str) -> dict:
    bot = make_bot()
    try:
        await bot.set_webhook(
            url=f"https://{host}/api/telegram",
            secret_token=SECRET,
            allowed_updates=["message", "callback_query"],
        )
        await bot.set_my_commands(commands())
        info = await bot.get_webhook_info()
        me = await bot.get_me()
        return {"bot": me.username, "webhook": info.url, "pending": info.pending_update_count,
                "last_error": info.last_error_message}
    finally:
        await bot.session.close()


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        given = self.headers.get("X-Setup-Secret", "")
        if not SECRET or not hmac.compare_digest(given, SECRET):
            return self._reply(403, {"error": "forbidden"})
        host = self.headers.get("x-forwarded-host") or self.headers.get("Host", "")
        self._reply(200, asyncio.run(_setup(host)))

    def _reply(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)
