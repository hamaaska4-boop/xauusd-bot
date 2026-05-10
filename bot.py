import requests
import time

TOKEN = "8566810402:AAF-cdeCg0mUWuIKqEPobRFhhmM3TYDxfzs"
CHAT_ID = "1799218177"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_candles():
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": "XAUUSDT", "interval": "15m", "limit": 3}
    r = requests.get(url, params=params)
    return r.json()

def calc_ema(prices, period):
    k = 2 / (period + 1)
    ema = prices[0]
    for p in prices[1:]:
        ema = p * k + ema * (1 - k)
    return ema

last_signal = ""

while True:
    try:
        candles = get_candles()
        closes = [float(c[4]) for c in candles]
        
        fast_prev = calc_ema(closes[:2], 20)
        fast_curr = calc_ema(closes[:3], 20)
        slow_prev = calc_ema(closes[:2], 50)
        slow_curr = calc_ema(closes[:3], 50)

        if fast_prev < slow_prev and fast_curr > slow_curr:
            if last_signal != "BUY":
                send_message("🟢 BUY SIGNAL ON XAUUSD")
                last_signal = "BUY"

        elif fast_prev > slow_prev and fast_curr < slow_curr:
            if last_signal != "SELL":
                send_message("🔴 SELL SIGNAL ON XAUUSD")
                last_signal = "SELL"

    except Exception as e:
        print(e)

    time.sleep(60)
