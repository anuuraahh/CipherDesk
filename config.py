"""
Central Configuration: loads environment variables and exposes a shared Groq-backed LLM instance used by all agents.

"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
EXA_API_KEY = os.getenv("EXA_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found. Check your .env file.")

if not EXA_API_KEY:
    raise EnvironmentError("EXA_API_KEY not found. Check your .env file.")

def get_llm(temperature: float = 0.3):
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=temperature,
        groq_api_key=GROQ_API_KEY
    )
    
    