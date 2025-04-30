import requests
from datetime import datetime, timedelta

def is_price_dropping(hours=6):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",              # get up to 24h of prices
        "interval": "hourly"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        prices = data.get("prices", [])
        if len(prices) < hours + 1:
            raise ValueError("Not enough hourly price data received.")

        # Get only the last (hours + 1) entries
        recent = prices[-(hours + 1):]
        closes = [price[1] for price in recent]

        is_dropping = all(closes[i] < closes[i - 1] for i in range(1, len(closes)))
        start_price = closes[0]
        end_price = closes[-1]
        percentage_change = ((end_price - start_price) / start_price) * 100
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        if is_dropping:
            print(f"[{timestamp}] BTC has been dropping continuously for {hours} hours.")
        else:
            print(f"[{timestamp}] BTC has NOT been dropping continuously for {hours} hours.")

        print(f"Start Price: ${start_price:.2f}")
        print(f"Current Price: ${end_price:.2f}")
        print(f"Change: {percentage_change:.2f}%")

    except Exception as e:
        print(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}] ERROR: {e}")

if __name__ == "__main__":
    is_price_dropping()
