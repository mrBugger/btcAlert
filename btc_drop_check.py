import requests
from datetime import datetime

def is_price_dropping(symbol="BTCUSDT", hours=6):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": "1h",
        "limit": hours + 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    closes = [float(candle[4]) for candle in data]

    # Track if price is dropping and calculate percentage change
    is_dropping = True
    for i in range(1, len(closes)):
        if closes[i] >= closes[i - 1]:
            is_dropping = False
            break

    start_price = closes[0]
    end_price = closes[-1]
    percentage_change = ((end_price - start_price) / start_price) * 100

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if is_dropping:
        print(f"[{timestamp}] BTC has been dropping continuously for {hours} hours.")
        print(f"Start Price: ${start_price:.2f}")
        print(f"Current Price: ${end_price:.2f}")
        print(f"Change: {percentage_change:.2f}%")
    else:
        print(f"[{timestamp}] BTC has NOT been dropping continuously for {hours} hours.")
        print(f"Start Price: ${start_price:.2f}")
        print(f"Current Price: ${end_price:.2f}")
        print(f"Change: {percentage_change:.2f}%")

if __name__ == "__main__":
    is_price_dropping()
