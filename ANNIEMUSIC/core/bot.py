import asyncio
import os
import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


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

        # Removed Telegram logging to LOGGER_ID

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name} (@{self.username})")
