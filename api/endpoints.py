import os
from dotenv import load_dotenv
load_dotenv()

finnhub_key = os.getenv("finnhub_key")


finnhub_baseUrl = "https://finnhub.io/api/v1"
polymarket_baseUrl = "https://gamma-api.polymarket.com"

finnhub_endpoints = {
    "profile": f"{finnhub_baseUrl}/stock/profile2",
    "quote": f"{finnhub_baseUrl}/quote",
    "insider_trades": f"{finnhub_baseUrl}/stock/insider-transactions"
}
polymarket_endpoints = {
    "events": f"{polymarket_baseUrl}/events",
    "event_byId": f"{polymarket_baseUrl}/events"
}