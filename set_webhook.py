#!/usr/bin/env python3
"""
Script to set or delete Telegram webhook.
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from bot.telegram_client import set_webhook, delete_webhook

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "delete":
        print("Deleting webhook...")
        success = delete_webhook()
        if success:
            print("Webhook deleted.")
        else:
            print("Failed to delete webhook.")
    else:
        url = os.environ.get("WEBHOOK_URL")
        if not url:
            print("ERROR: WEBHOOK_URL environment variable not set.")
            sys.exit(1)
        print(f"Setting webhook to {url}...")
        success = set_webhook(url)
        if success:
            print("Webhook set successfully.")
        else:
            print("Failed to set webhook.")