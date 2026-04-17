"""
Configuration and environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required")

# OpenAI base URL (for LongCat or other compatible APIs)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

# Webhook URL (must be HTTPS)
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

# OpenAI model
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "LongCat-Flash-Chat")

# Memory settings
MAX_HISTORY_PER_USER = int(os.environ.get("MAX_HISTORY_PER_USER", 20))

# Telegram API
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"