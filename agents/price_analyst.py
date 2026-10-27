"""
Price Analyst Agent 
Fetches current + historical price data and generates a technical
narrative around it (trend, volatitlity range, momentum).
"""

from langchain_core.messages import SystemMessage, HumanMessage
from config import get_llm
from tools.price_tool import get_current_price, get_historical_prices

SYSTEM_PROMPT = """ You are the Price Analyst agent in a crypto analysis system.
You'll receive current price stats and historical price stats for a coin.

Write a short technical summary covering:
1. Current price and 24h movement
2. Trend over the analyzed period (up/down/sideways, magnitude)
3. Volatility (range between period high and low)

Be concise, quantitative, and avoid speculation beyond the numbers given."""


def analyze_price(coin: str, days: int = 30) -> dict:
    current = get_current_price(coin)
    historical = get_historical_prices(coin, days=days)

    data_summary = (
        f"Current price: ${current.get('usd')}\n"
        f"24h change: {current.get('usd_24h_change', 0):.2f}%\n"
        f"Market cap: ${current.get('usd_market_cap', 0):,.0f}\n"
        f"24h volume: ${current.get('usd_24h_vol', 0):,.0f}\n\n"
        f"Over the last {days} days:\n"
        f"Start price: ${historical['start_price']:.2f}\n"
        f"End price: ${historical['end_price']:.2f}\n"
        f"% change: {historical['pct_change']}%\n"
        f"Period high: ${historical['period_high']:.2f}\n"
        f"Period low: ${historical['period_low']:.2f}\n"
    )

    llm = get_llm(temperature=0.2)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Coin: {coin}\n\n{data_summary}"),
    ]
    response = llm.invoke(messages)

    return {
        "current": current,
        "historical": historical,
        "summary": response.content.strip()
    }