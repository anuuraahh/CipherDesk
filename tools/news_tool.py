"""
Fetches real-time crypto news using Exa's neural search API
"""
from exa_py import Exa
from config import EXA_API_KEY

exa_client = Exa(api_key=EXA_API_KEY)

def search_crypto_news(coin: str, num_results: int = 6) -> list[dict]:
    """
    Searches for recent news articles about a given cryptocurrency.
    Returns a list of {title, url, published_date, snippet}.
    """
    query = f"Latest news and market analysis about {coin} cryptocurrency"

    results = exa_client.search_and_contents(
        query,
        num_results=num_results,
        type="neural",
        category="news",
        text={"max_characters": 500},
    )

    articles = []
    for r in results.results:
        articles.append({
            "title": r.title,
            "url": r.url,
            "published_date": getattr(r, "published_date", None),
            "snippet": (r.text or "").strip(),
        })
        
    return articles