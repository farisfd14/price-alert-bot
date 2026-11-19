# price-alert-bot

A tiny Python bot that checks a stock price once a day and messages me
on Telegram only when something CHANGED (crossed my threshold, or back
to normal). No spam, no dashboards, no servers - one script + Windows
Task Scheduler.

## How it works

1. `config.ini` says what to watch: ticker + "alert me below X / above Y"
2. `src/price.py` fetches the latest price (yfinance, with patient retries -
   Yahoo rate-limits by IP)
3. `src/main.py` maps the price to BELOW / NORMAL / ABOVE and compares
   with `state.txt` (what it said last run)
4. Only on a CHANGE: `src/notify.py` sends a Telegram message and saves
   the new state. No change = no message.

## Setup

`pip install -r requirements.txt`

1. Create a bot with @BotFather on Telegram, get the token
2. Message your bot once, then open
   `https://api.telegram.org/bot<TOKEN>/getUpdates` in a browser to find
   your chat_id
3. Put both values in `.env` (see `.env.example` pattern - never commit .env)
4. Edit `config.ini` (ticker + thresholds)

## Run it

`python src/main.py`

## Run it every day

Windows Task Scheduler, daily trigger, action:
- Program: full path to `python.exe`
- Arguments: `C:\...\price-alert-bot\src\main.py`
- Start in: `C:\...\price-alert-bot`

## Lessons baked in

- retries + fallback thinking for network calls (Yahoo rate limits)
- proxy handling: bypassed for yfinance (broke stock-lab), kept for
  Telegram (blocked without it in China)
- state file so an alert bot only speaks on changes
- secrets in .env, never in code, never on GitHub

## .env example

- TELEGRAM_TOKEN=paste-your-token-here
- TELEGRAM_CHAT_ID=paste-your-chat-id-here