"""
Customer Communicator Agent

Takes free-form user input (eg. "How's bitcoin doing lately?) and 
extracts a structured request: which coin, and how many days of history.

""" 
import json
from langchain_core.messages import SystemMessage, HumanMessage
from config import get_llm

SYSTEM_PROMPT = """You are the Customer Communicator agent in a crypto analysis system.
Your job: read the user's request and extract structured parameters.

Respond with ONLY a JSON object, no other text, in this exact format:
{
    "coin": "<coin name or symbol>, lowercase>", "days": <integer, default 30 if not specified>
}

Examples:
User: "How is Bitcoin doing this month?" -> {"coin": "bitcoin", "days": 30}
User: "Give me a report on ETH for the last week" -> {"coin": "eth", "days": 7}
User: "solana trend past 90 days" -> {"coin": "solana", "days": 90}
"""

def parse_user_request(user_input: str) -> dict:
    llm = get_llm(temperature=0)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_input)
    ]
    response = llm.invoke(messages)
    raw = response.content.strip()
    
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()
    
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"coin": "bitcoin", "days": 30}
        
    parsed.setdefault("coin", "bitcoin")
    parsed.setdefault("days", 30)
    return parsed