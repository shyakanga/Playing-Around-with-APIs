from api.polymarket import get_eventById
from logic.processor import analyze_insider_trades, mapIndustry_to_polymarketTag, get_companyInfo, parse_polymarket_events

from cli.cli import display_events, display_company_info, display_insider_page, paginate_list, paginate_remote_events



def polymarket_menu():
    print("\n   Polymarket Event Search Menu")
    print(" (1) Search event by Id (eg: 02338)")
    print(" (2) Browse all active events")
    print(" (3) Browse by category (eg: politics, crypto, sports....)")
    choice = input("Select your option: ").strip()
    
    if choice == "1":
        event_id = input("Enter the Id of the event you would like to search: ").strip()
        raw = get_eventById(event_id)
        
        if not raw:
            print("Event not found")
            return
        display_events(parse_polymarket_events([raw]))
    elif choice == "2":
        paginate_remote_events()
    elif choice == "3":
        category = input("Enter category (eg: politics, sports, tech): ")
        if category:
            paginate_remote_events(tag_slug=category)
            

def browse_insider_trading():
    ticker = input("\nEnter company stock ticker (eg: AAPL, NVDA): ").strip().upper()
    if not ticker:
        return
    
    result = analyze_insider_trades(ticker)
    if not result:
        print(f"No data found about {ticker}")
        return
    
    profile = result["profile"]
    trades = result["trades"]
    current_price = result["current_price"]
    
    paginate_list(
        trades,
        render_function=lambda page_items: display_insider_page(page_items, ticker)
    )
    
    industry = profile["industry"]
    polymarket_tag = mapIndustry_to_polymarketTag(industry)
    
    follow = input(f"Would you like to see polymarkets events about {industry}? {profile["name"]} is in it! (y/n): ")
    
    if follow == "y":
        paginate_remote_events(tag_slug=polymarket_tag)
        


def company_lookup():
    ticker = input("\nEnter company ticker. (eg: MSFT, TSL): ").strip().upper()
    
    if not ticker:
        return
    
    profile = get_companyInfo(ticker)
    if not profile:
        print(f"Info about {ticker} not found!")
        return
    
    display_company_info(profile)



def main():
    while True:
        print("\n"+"-"*50)
        print("     INSIDER TRADING SEARCH      ")
        print("\n"+"-"*50)
        print("1. Search Polymarket Events (by ID, Category, or Browse All)")
        print("2. Insider Trading by Company (e.g., NVDA, LMT, AAPL)")
        print("3. Company Info by ticker (e.g., MSFT, PFE, TSLA)")
        print("(x) Quit app")
        
        choice = input("\nChoose an option: ").strip()
        
        try:
            if choice == "1":
                polymarket_menu()
            elif choice == "2":
                browse_insider_trading()
            elif choice == "3":
                company_lookup()
            elif choice == "x":
                break
            else:
                print("Enter a valid option: ")
        except Exception as errr:
            print(f"\nAn error occured {errr}")
            
if __name__ == "__main__":
    main()