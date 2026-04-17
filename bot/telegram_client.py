"""
Telegram API client.
"""
import logging
import requests
from typing import List, Tuple, Optional
from bot.config import TELEGRAM_API_URL

logger = logging.getLogger(__name__)

def send_message(chat_id: int, text: str, parse_mode: str = "HTML") -> bool:
    """
    Send a text message to a Telegram chat.
    """
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to send message to {chat_id}: {e}")
        return False

def send_buttons(
    chat_id: int,
    text: str,
    buttons: List[List[Tuple[str, str]]],
    parse_mode: str = "HTML"
) -> bool:
    """
    Send an inline keyboard with buttons.
    Each button is a tuple (text, callback_data).
    """
    inline_keyboard = []
    for row in buttons:
        inline_keyboard.append([
            {"text": btn_text, "callback_data": callback_data}
            for btn_text, callback_data in row
        ])
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": inline_keyboard},
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to send buttons to {chat_id}: {e}")
        return False

def edit_message_reply_markup(
    chat_id: int,
    message_id: int,
    reply_markup: Optional[dict]
) -> bool:
    """
    Edit the reply markup of an existing message (e.g., remove buttons).
    """
    url = f"{TELEGRAM_API_URL}/editMessageReplyMarkup"
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": reply_markup if reply_markup is not None else {},
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Failed to edit message reply markup: {e}")
        return False

def set_webhook(url: str) -> bool:
    """
    Set Telegram webhook to the given URL.
    """
    webhook_url = f"{TELEGRAM_API_URL}/setWebhook"
    payload = {"url": url}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Webhook set to {url}")
        return True
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        return False

def delete_webhook() -> bool:
    """
    Delete the current webhook.
    """
    url = f"{TELEGRAM_API_URL}/deleteWebhook"
    try:
        response = requests.post(url, timeout=10)
        response.raise_for_status()
        logger.info("Webhook deleted")
        return True
    except Exception as e:
        logger.error(f"Failed to delete webhook: {e}")
        return False