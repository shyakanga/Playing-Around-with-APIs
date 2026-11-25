import requests
from fetching.endpoints import finnhub_endpoints, finnhub_key

header = { "X-Finnhub-Token" : finnhub_key}

def get_company_info(ticker):
    response = requests.get(
        finnhub_endpoints["profile"], 
        params={"symbol": ticker.upper()},
        headers=header,
        timeout=10
    )
    
    response.raise_for_status()
    return response.json()

def get_current_price(ticker):
    response = requests.get(
        finnhub_endpoints["quote"],
        params={"symbol": ticker.upper()},
        headers=header,
        timeout=10
    )
    
    response.raise_for_status()
    data = response.json()
    return float(data.get("c", 0.0))

def get_insider_trades(ticker):
    response = requests.get(
        finnhub_endpoints["insider_trades"],
        params={"symbol": ticker.upper()},
        headers=header,
        timeout=10
    )
    response.raise_for_status()
    return response.json().get("data", [])
