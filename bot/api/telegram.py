"""Vercel serverless function: Telegram sends every update here (webhook).

Telegram adds the X-Telegram-Bot-Api-Secret-Token header we registered in
api/setup.py; anything without it is refused, so nobody else can feed the
bot fake updates.
"""

import asyncio
import hmac
import json
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.bootstrap import make_bot, make_dispatcher  # noqa: E402
from app.fsm_storage import SupabaseStorage  # noqa: E402

SECRET = os.environ.get("WEBHOOK_SECRET", "")
MAX_BODY = 1_000_000

# One dispatcher per warm process; its routers can't be attached twice.
_dp = make_dispatcher(SupabaseStorage())


async def _process(update: dict) -> None:
    bot = make_bot()  # its HTTP session belongs to this event loop, so one per request
    try:
        await _dp.feed_raw_update(bot, update)
    finally:
        await bot.session.close()


class handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        token = self.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not SECRET or not hmac.compare_digest(token, SECRET):
            return self._reply(403, b"forbidden")
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._reply(400, b"bad request")
        try:
            update = json.loads(self.rfile.read(length))
        except ValueError:
            return self._reply(400, b"bad request")
        try:
            asyncio.run(_process(update))
        except Exception:
            # Answer 200 anyway: a non-2xx makes Telegram resend the same update forever.
            logging.exception("update failed")
        self._reply(200, b"ok")

    def do_GET(self) -> None:
        self._reply(200, b"SilkRoad Exchange bot webhook")

    def _reply(self, code: int, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)
