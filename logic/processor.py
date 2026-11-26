import json
from api.finnhub import (
    get_company_info,
    get_current_price,
    get_insider_trades
)


industry_to_polymarketTag = {
    "aerospace & defense": "geopolitics",
    "biotechnology": "science",
    "pharmaceuticals": "health",
    "health care": "health",
    "semiconductors": "tech",
    "technology": "tech",
    "software": "tech",
    "banking": "business",
    "financial services": "business",
    "energy": "business",
    "oil & gas": "business",
    "media": "pop-culture",
    "entertainment": "pop-culture",
    "hotels, restaurants & leisure": "sports"
}



def get_companyInfo(ticker):
    raw = get_company_info(ticker)
    
    if not raw:
        return None
    
    return {
        "ticker": raw.get("ticker"),
        "name": raw.get("name", "N/A"),
        "market_cap": raw.get("marketCapitalization", 0),
        "website": raw.get("weburl", "N/A"),
        "industry": raw.get("finnhubIndustry", "General"),
    }
    

def analyze_insider_trades(ticker):
    profile = get_companyInfo(ticker)
    
    if not profile:
        return None
    
    current_price = get_current_price(ticker)
    raw_trades = get_insider_trades(ticker)
    
    processed_trades = []
    for trade in raw_trades:
        difference = trade.get("change") or 0
        if difference == 0:
            continue
        
        action = "Bought" if difference > 0 else "Sold"
        trade_price = float(trade.get("transactionPrice") or 0)
        
        if trade_price > 0 and current_price > 0:
            difference_string = f"{(((current_price - trade_price)/ trade_price) * 100):+.1f}%"
        else:
            difference_string = "Grant"
        
        processed_trades.append({
            "name": trade.get("name", "Uknown"),
            "action": action,
            "shares": abs(difference),
            "trade_price": trade_price,
            "current_price": current_price,
            "percent_diff": difference_string,
            "date": trade.get("transactionDate", "N/A")
        })
        
    return {
        "profile": profile,
        "current_price": current_price,
        "trades": processed_trades
    }


def parse_polymarket_events(raw_events):
    parsed = []
    for event in raw_events:
        market_summary = []
        for market in event.get("markets", []):
            question = market.get("question", "")
            try: 
                outcomes = json.loads(market.get("outcomes") or "[]")
                prices = json.loads(market.get("outcomePrices") or "[]")
                odds = [f"{outc}: {float(pri) *100 :.1f}%" for outc,pri in zip(outcomes,prices)]
                market_summary.append(f"{question} -> {" | ".join(odds)}")
            except (ValueError, TypeError):
                continue
        parsed.append({
            "id": event.get("id", "N/A"),
            "title": event.get("title", "No title"),
            "volume": float(event.get("volume", 0) or 0),
            "ends": (event.get("endDate") or "N/A")[:10],
            "outcomes":market_summary[:3] 
        })
        
    return parsed


def mapIndustry_to_polymarketTag(industry):
    if not industry:
        return "business"
    key = industry.strip().lower()
    for industry_key, tag in industry_to_polymarketTag.items():
        if industry_key in key:
            return tag
    return "business"

