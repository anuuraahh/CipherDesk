"""
FastAPI backend for the Crypto Analysis Agent System.
Exposes each agent as its own endpoint so a frontend can show real,
step-by-step progress instead of one long blocking call.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.communicator import parse_user_request
from agents.news_analyst import analyze_news
from agents.price_analyst import analyze_price
from agents.report_writer import write_report

app = FastAPI(title="Crypto Analysis Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class CoinDaysRequest(BaseModel):
    coin: str
    days: int = 30


class ReportRequest(BaseModel):
    coin: str
    price_analysis: dict
    news_analysis: dict


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Crypto Analysis API is running"}


@app.post("/parse")
def parse(request: QueryRequest):
    try:
        return parse_user_request(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/news")
def news(request: CoinDaysRequest):
    try:
        return analyze_news(request.coin)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/price")
def price(request: CoinDaysRequest):
    try:
        return analyze_price(request.coin, days=request.days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report")
def report(request: ReportRequest):
    try:
        text = write_report(request.coin, request.price_analysis, request.news_analysis)
        return {"report": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))