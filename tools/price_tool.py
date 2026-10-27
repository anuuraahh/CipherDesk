"""
Fetches current + historical price data from CoinGecko's free public API.
No API key required. Rate limit: ~10-30 calls/min on free tier.

"""

import requests

COINGECKO_BASE = "https://api.coingecko.com/api/v3"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

SYMBOL_MAP = {
    "btc": "bitcoin", "bitcoin": "bitcoin",
    "eth": "ethereum", "ethereum": "ethereum",
    "sol": "solana", "solana": "solana",
    "doge": "dogecoin", "dogecoin": "dogecoin",
    "xrp": "ripple", "ripple": "ripple",
    "ada": "cardano", "cardano": "cardano",
    "bnb": "binancecoin", "binancecoin": "binancecoin",
}

def resolve_coin_id(coin: str) -> str:
    key = coin.strip().lower()
    return SYMBOL_MAP.get(key, key)

def get_current_price(coin: str, vs_currency: str = "usd") -> dict:
    coin_id = resolve_coin_id(coin)
    url = f"{COINGECKO_BASE}/simple/price"
    params = {
       "ids": coin_id,
       "vs_currencies": vs_currency,
       "include_24hr_change": "true",
       "include_market_cap": "true",
       "include_24hr_vol": "true", 
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data =  resp.json()
    if coin_id not in data:
        raise ValueError(f"Could not find price data for '{coin} (resolved id: {coin_id})")
    return {"coin_id": coin_id, **data[coin_id]}

def get_historical_prices(coin: str, days: int = 30, vs_currency: str = "usd") -> dict:
    """Returns daily price points over the given window."""
    coin_id = resolve_coin_id(coin)
    url = f"{COINGECKO_BASE}/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days,
        "interval": "daily"
    }
    resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    prices = data.get("prices", [])
    if not prices:
        raise ValueError(f"No historical data found for '{coin}'")
    
    start_price = prices[0][1]
    end_price = prices[-1][1]
    pct_change = ((end_price - start_price) / start_price) * 100 if start_price else 0
    high = max(p[1] for p in prices)
    low = min(p[1] for p in prices)
    
    return {
        "coin_id": coin_id,
        "days": days,
        "start_price": start_price,
        "end_price": end_price,
        "pct_change": round(pct_change, 2),
        "period_high": high,
        "period_low": low,
        "num_points": len(prices),
    }