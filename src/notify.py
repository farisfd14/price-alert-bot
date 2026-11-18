# src/notify.py
# Milestone 2: send a message to yourself on Telegram.
# You need TWO things for this to work:
# TOKEN     - from BotFather when you created the bot
# CHAT_ID   - a number that identifies YOUR account (we get it below)

import os

import requests
from dotenv import load_dotenv

load_dotenv()   # finds .env and loads TELEGRAM_TOKEN / TELEGRAM_CHAT_ID

# paste your real values here (keep the quotes!)
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# never commit real secrets to GitHub - we fix this in README step
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


def send_message(text: str):
    """Send `text` to my Telegram. Returns True if Telegram accepted it."""
    session = requests.Session()
    session.trust_env = False   # our trusted proxy bypass again
    resp = session.post(TELEGRAM_URL, data={
        "chat_id": CHAT_ID,
        "text": text,
    }, timeout=30)
    return resp.status_code == 200


if __name__ == "__main__":
    ok = send_message("hello from price-alert-bot! this is a test.")
    print("sent!" if ok else "failed - check .env values")