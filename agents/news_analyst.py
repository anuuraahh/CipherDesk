"""
News Analyst Agent
Fetches recent news via Exa, then uses the LLM to summarize sentiment
and key themes.

"""
from langchain_core.messages import SystemMessage, HumanMessage
from config import get_llm
from tools.news_tool import search_crypto_news

SYSTEM_PROMPT = """ You are the News Analyst agent in a crypto analysis system.
You'll receive a list of recent news articles about a cryptocurrency.
Summarize:
1. Overall sentiment (bullish / bearish / neutral / mixed)
2. 3-5 key themes or events driving the news
3. Any notable risks or catalysts mentioned

Be concise and factual. Base your summary only on the provided articles."""


def analyze_news(coin: str) -> dict:
    articles = search_crypto_news(coin)
    
    if not articles:
        return {
            "articles": [],
            "summary": "No recent news articles found."
        }
    articles_text = "\n\n".join(
        f"Title: {a['title']}\nDate: {a['published_date']}\nSnippet: {a['snippet']}"
        for a in articles
    )
    
    llm = get_llm(temperature=0.3)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Cryptocurrency: {coin}\n\nArticles:\n{articles_text}")
    ]
    
    response = llm.invoke(messages)
    
    return {
        "articles": articles,
        "summary": response.content.strip()
    }
    
    