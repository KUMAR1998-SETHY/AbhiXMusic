import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import asyncio
import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER

# ------------------- DUMMY HTTP SERVER FOR RENDER -------------------
PORT = int(os.environ.get("PORT", 8080))  # Render sets PORT automatically

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    server.serve_forever()

# Run HTTP server in a separate thread
threading.Thread(target=run_server, daemon=True).start()
# ---------------------------------------------------------------------

class JARVIS(Client):
    def __init__(self):
        super().__init__(
            name="AnnieXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            workers=30,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot client initialized.")

    async def _auto_restart(self):
        interval = getattr(config, "RESTART_INTERVAL", 86400)  # fallback 24 hours
        while True:
            await asyncio.sleep(interval)
            try:
                await self.disconnect()
                await self.start()
                LOGGER(__name__).info("🔄 Pyrogram session auto-restarted successfully.")
            except Exception as exc:
                LOGGER(__name__).warning(f"Auto-restart failed: {exc}")

    async def start(self):
        await super().start()
        asyncio.create_task(self._auto_restart())

        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name} (@{self.username})")
