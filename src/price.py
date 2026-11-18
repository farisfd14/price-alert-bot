# src/price.py
# Fetch the latest price of one ticker with yfinance.
# Stock-lab lessons baked in: proxy bypass + retry on rate limit
# because Yahoo throttles aggressively and the bot runs unattended.

import time

import requests
import yfinance as yf

MAX_ATTEMPTS = 3
WAIT_SECONDS = 30   # wait between retires; Yahoo's limit cools down fast


def get_price(ticker: str) -> float:
    """Return the most recent closing price of `ticker` as a float."""
    session = requests.Session()
    session.trust_env = False   # bypass system proxy - it broke stock-lab
    data = yf.Ticker(ticker, session=session)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            close_col = data.history(period="5d")["Close"]
            return float(close_col.iloc[-1])
        except Exception as error:
            print(f"attempt {attempt} failed: {error}")
            if attempt < MAX_ATTEMPTS:
                print(f"waiting {WAIT_SECONDS}s before retry...")
                time.sleep(WAIT_SECONDS)
    raise RuntimeError("could not fetch price after all retries")

if __name__ == "__main__":
    print(get_price("TSLA"))