import asyncio
import logging
import secrets
import requests
from typing import Dict, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# In-memory storage for simplicity (Use DB in production)
# Mapping: token -> chat_id
telegram_links: Dict[str, str] = {}
# Mapping: token -> created_at (for cleanup, ignored for now)

class TelegramService:
    last_update_id = 0
    is_running = False

    @staticmethod
    def generate_link_token() -> str:
        """Generate a random 8-char token for linking."""
        return secrets.token_urlsafe(8)

    @staticmethod
    def get_bot_link(token: str) -> str:
        """Generate the t.me link with start parameter."""
        # We need the bot username. Since we don't have it in config, we can fetch it or hardcode.
        # Ideally, fetch "getMe" once on startup. For now, assuming user knows it or we fetch it.
        # Let's fetch it dynamically or just return a generic format if lazy.
        # Better: Fetched during polling or startup.
        # For now, let's use a placeholder or ask user to put username in env? 
        # Actually, getMe is cheap.
        return f"https://t.me/KhalifAppsBot?start={token}" 

    @staticmethod
    def get_chat_id_by_token(token: str) -> Optional[str]:
        return telegram_links.get(token)

    @staticmethod
    async def start_polling():
        """Background task to poll Telegram updates."""
        TelegramService.is_running = True
        logger.info("Starting Telegram Polling...")
        while TelegramService.is_running:
            try:
                await TelegramService._poll_updates()
            except Exception as e:
                logger.error(f"Telegram polling error: {e}")
            
            await asyncio.sleep(2) # Poll every 2 seconds

    @staticmethod
    async def _poll_updates():
        if not settings.telegram_bot_token:
            return

        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/getUpdates"
        params = {
            "offset": TelegramService.last_update_id + 1,
            "timeout": 10 # Long polling timeout
        }
        
        # Requests is blocking, so we run it in executor or use aiohttp. 
        # For simple use case in FastAPI, we can use run_in_executor.
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.get(url, params=params, timeout=15))
        
        if response.status_code != 200:
            logger.error(f"Telegram API Error: {response.text}")
            return

        data = response.json()
        if not data.get("ok"):
            return

        for result in data.get("result", []):
            update_id = result["update_id"]
            TelegramService.last_update_id = max(TelegramService.last_update_id, update_id)

            if "message" in result and "text" in result["message"]:
                text = result["message"]["text"]
                chat_id = str(result["message"]["chat"]["id"])
                
                # Check for /start COMMAND
                if text.startswith("/start"):
                    parts = text.split()
                    if len(parts) > 1:
                        token = parts[1]
                        # Store the link!
                        telegram_links[token] = chat_id
                        logger.info(f"Linked Token {token} to Chat ID {chat_id}")
                        
                        # Optional: Reply to user
                        TelegramService._send_reply(chat_id, "Berhasil terhubung! Akun Anda siap menerima OTP. ✅")

    @staticmethod
    def _send_reply(chat_id: str, text: str):
        url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text})

    @staticmethod
    def stop_polling():
        TelegramService.is_running = False
