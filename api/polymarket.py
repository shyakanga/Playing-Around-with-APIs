import requests
from api.endpoints import polymarket_endpoints

def get_eventById(event_id):
    url = f"{polymarket_endpoints["event_byId"]}/{event_id}"
    response = requests.get(url, timeout=10)
    
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

def get_events(limit=10, offset=0, tag_slug=None):
    params_p = {
        "active":"true",
        "limit":limit,
        "closed":"false",
        "offset":offset,
        "order":"volume24hr"
    }
    
    if tag_slug:
        params_p["tag_slug"] = tag_slug.strip().lower()
    
    response = requests.get(polymarket_endpoints["events"], params=params_p, timeout=10)
    response.raise_for_status()
    return response.json()

