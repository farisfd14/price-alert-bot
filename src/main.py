# src/main.py
# Milestone 3: the complete alert logic.
#
#   1. read config.ini (ticker + thresholds)
#   2. fetch the current price
#   3. compare with thresholds -> today's status
#   4. read state.txt (what we said yesterday)
#   5. if the status CHANGED -> send Telegram alert, save new state
#      if nothing changed -> stay quiet (no spam)
#
# The bot's golden rule: only speak when something changed.

import configparser
import os

from notify import send_message
from price import get_price

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(PROJECT_ROOT, "state.txt")


def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(PROJECT_ROOT, "config.ini"))
    return {
        "ticker": config["alert"]["ticker"].strip().upper(),
        "below": float(config["alert"]["below"]),
        "above": float(config["alert"]["above"]),
    }


def decide_status(price, below, above):
    """Map a price to one of three situations."""
    if price < below:
        return "BELOW"
    if price > above:
        return "ABOVE"
    return "NORMAL"


def load_state():
    """What we said last time. Missing file = first run ever."""
    if not os.path.exists(STATE_PATH):
        return None
    with open(STATE_PATH, encoding="utf-8") as f:
        return f.read().strip()


def save_state(status):
    """Remember today's sattus for tomorrow's run."""
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        f.write(status)


def main():
    cfg = load_config()
    print(f"checking {cfg['ticker']}...")

    price = get_price(cfg["ticker"])
    status = decide_status(price, cfg["below"], cfg["above"])
    print(f"price {price:.2f} -> status {status}")

    previous = load_state()
    if status == previous:
        print("nothing changed sicne last check - staying quiet")
        return

    # status changed (or first run) -> tell me
    messages = {
        "BELOW": f"📉 {cfg['ticker']} dropped below {cfg['below']:.0f}! "
                 f"Now at {price:.2f}.",
        "ABOVE": f"📈 {cfg['ticker']} rose above {cfg['above']:.0f}! "
                 f"Now at {price:.2f}.",
        "NORMAL": f"✅ {cfg['ticker']} is back in the normal range "
                  f"({cfg['below']:.0f}-{cfg['above']:.0f}). Now at {price:.2f}.",
    }
    ok = send_message(messages[status])
    if ok:
        save_state(status)
        print(f"alert sent: {status}")
    else:
        print("telegram failed - keeping old state, will retry next run")


if __name__ == "__main__":
    main()