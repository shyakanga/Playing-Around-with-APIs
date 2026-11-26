from api.polymarket import get_events
# from fetching.finnhub import get_insider_trades
from logic.processor import parse_polymarket_events


def display_company_info(profile):
    print("\n" + "-" * 50)
    print(f"    Company Profile:  {profile["name"]} ({profile["ticker"]})")
    print("-" * 50)
    print(f"    Industry    : {profile["industry"]}")
    print(f"    Marketcap:  : {profile['market_cap']:,.2f} Mil")
    print(f"    Website     : {profile['website']}")
    print("-"*50)


def display_insider_page(trades, ticker):
    print(f"\n --- Insider Trades for {ticker.upper()} --- ")
    print(f"{'DATE':<12} | {'INSIDER':<22} | {'ACTION':<6} | {'SHARES':>10} | {'AT PRICE':>10} | {'VS NOW':>11}")
    
    for tr in trades:
        price_str = f"${tr['trade_price']:,.2f}" if tr['trade_price'] > 0 else "$0.00"
        print(
            f"{tr['date']:<12} | {tr['name'][:22]:<22} | {tr['action']:<6} | "
            f"{tr['shares']:>10,} | {price_str:>10} | {tr['percent_diff']:>11}"
        )


def display_events(events):
    if not events:
        print("No Polymarket events found for your input")
        return
    
    print("\n"+ "-"*50)
    for event in events:
        print(f"ID: {event['id']} {event['title']}")
        print(f"Volume: {event['volume']:,.0f}  |    End date: {event['ends']}")
        for line in event['outcomes']:
            print(f"    - {line}")
        
        print("-"*50)


def paginate_list(items, render_function, default_size=10):
    if not items:
        print("\n No Records found")
        return
    
    page_size = default_size
    page = 0
    
    while True:
        total_pages = len(items) + page_size- 1
        start = page * page_size
        end = start + page_size
        
        render_function(items[start:end])
        print(f"\nPage {page + 1} of {total_pages} (Showing {page_size} per page | Total: {len(items)})")
        
        cmd = input("(N)Next,   (P) Prev,   (B) Back").strip().lower()
        
        if cmd == "n" and page + 1 < total_pages:
            page += 1
        elif cmd == "p" and page > 0:
            page -= 1
        elif cmd == "b":
            break
        

def paginate_remote_events(tag_slug= None, default_size=5):
    limit = default_size
    offset = 0
    
    while True:
        raw = get_events(limit=limit, offset=offset, tag_slug=tag_slug)
        events = parse_polymarket_events(raw)
        display_events(events)
        
        page_num = (offset // limit) + 1
        label = f"Category: {tag_slug}" if tag_slug else "All Categories"
        print(f"Page {page_num} {label}: Limit page {limit}")
        
        cmd = input(f"(N)Next | (P)Prev | (B)Back:").strip().lower()
        
        if cmd == "n" and len(events) == limit:
            offset += limit
        elif cmd == "p" and offset >= limit:
            offset -= limit
        elif cmd == "b":
            break
