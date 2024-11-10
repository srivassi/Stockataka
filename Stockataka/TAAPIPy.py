import http.client
import json
from pprint import pprint

# Token for API authentication
token = "sk_live_KLTxJeItYDWnMh8tiyDEXHMVti9gSNto"

# Define sector and associated types
sectors = {
    "technology": ["AAPL", "GOOGL", "AMD", "MSFT", "NVDA", "META"],
    "health": ["AMGN", "GILD", "MRNA", "ISRG", "REGN", "ILMN"],
    "energy": ["ENPH", "FSLR", "FCX", "COP", "XOM", "OXY"],
    "raw_materials": ["FCX", "ALB", "NUE", "LAC", "NEM", "CCL"],
    "transport": ["TSLA", "LUV", "JBHT", "UPS", "CSX", "FDX"],
    "manufacturing": ["AMAT", "TXN", "HON", "INTC", "ADI", "LRCX"],
    "services": ["AMZN", "BKNG", "SBUX", "COST", "EBAY", "MAR"]
}

def fetch_data_from_api(path, api_key):
    """
    Helper function to fetch data from the API and handle errors.

    Parameters:
    - path: The query path for the API request.
    - api_key: The API key for authentication.

    Returns:
    - The decoded response data if successful, None if the request fails.
    """
    conn = http.client.HTTPSConnection("taapi.p.sulu.sh")
    headers = {'Accept': "application/json", 'Authorization': f"Bearer {api_key}"}
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()

    if res.status != 200:
        print(f"Request failed with status {res.status}: {res.reason}")
        return None

    data = res.read()
    try:
        return json.loads(data.decode("utf-8"))
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response.")
        return None


def get_candle_average_price(symbol, exchange, interval, backtrack, type):
    """
    Fetches the average price for a given symbol from the taapi API.

    Parameters:
    - symbol: The trading pair symbol (e.g., "AMZN").
    - exchange: The exchange name (e.g., "stocks").
    - interval: The time interval for each candle (e.g., "1w").
    - backtrack: The number of candles to backtrack.
    - type: The type of asset (e.g., "stocks").

    Returns:
    - The average price for the symbol for the given backtrack, or None if an error occurs.
    """
    path = f"/avgprice?exchange={exchange}&symbol={symbol}&interval={interval}&backtrack={backtrack}&type={type}"
    data = fetch_data_from_api(path, token)
    if data and 'value' in data:
        return data['value']
    print(f"Error: 'value' key missing in the response for backtrack={backtrack}.")
    return None


def get_sector(symbol):
    """
    Determines the sector for a given symbol.

    Parameters:
    - symbol: The stock symbol to check.

    Returns:
    - The sector to which the symbol belongs, or None if the symbol is not found.
    """
    for sector, symbols in sectors.items():
        if symbol in symbols:
            return sector
    return None

def get_full_company_name(symbol):
    """
    Given a company symbol, returns the full company name. This is a helper function for mapping symbols
    to full company names in the sectors list.

    Parameters:
    - symbol: The stock symbol (e.g., "AMZN").

    Returns:
    - The full company name (e.g., "Amazon").
    """
    company_mapping = {
        "AMZN": "Amazon",
        "COST": "Costco",
        "SBUX": "Starbucks",
        "BKNG": "Booking Holdings",
        "MAR": "Marriott",
        "EBAY": "eBay",
        "HON": "Honeywell",
        "AMAT": "Applied Materials",
        "LRCX": "Lam Research",
        "TXN": "Texas Instruments",
        "INTC": "Intel",
        "ADI": "Analog Devices",
        "FCX": "Freeport-McMoRan",
        "NEM": "Newmont Mining",
        "NUE": "Nucor",
        "ALB": "Albemarle",
        "LAC": "Lithium Americas Corp",
        "CCL": "Carnival Corporation",
        "TSLA": "Tesla",
        "LUV": "Southwest Airlines",
        "JBHT": "J.B. Hunt Transport Services",
        "UPS": "United Parcel Service",
        "CSX": "CSX Corporation",
        "FDX": "FedEx",
        "ENPH": "Enphase Energy",
        "FSLR": "First Solar",
        "MRNA": "Moderna",
        "ISRG": "Intuitive Surgical",
        "AMGN": "Amgen",
        "GILD": "Gilead Sciences",
        "REGN": "Regeneron Pharmaceuticals",
        "ILMN": "Illumina",
        "AAPL": "Apple",
        "GOOGL": "Google",
        "MSFT": "Microsoft",
        "NVDA": "NVIDIA",
        "META": "Meta",
    }

    return company_mapping.get(symbol, "Unknown Company")


def build_result():
    """
    Builds a nested result dictionary with sectors and company data.

    Returns:
    - A dictionary containing sector names as keys and their corresponding companies' details.
    """
    result = {}
    exchange = "stocks"  # Assuming all are stock exchanges
    interval = "1w"  # Weekly interval
    type = "stocks"  # Stock type

    # Define a dictionary of sectors with full company names
    sectors_full_name = {
        "services": ["Amazon", "Costco", "Starbucks", "Booking Holdings", "Marriott", "eBay"],
        "manufacturing": ["Honeywell", "Applied Materials", "Lam Research", "Texas Instruments", "Intel",
                          "Analog Devices"],
        "raw_materials": ["Freeport-McMoRan", "Newmont Mining", "Nucor", "Albemarle", "Lithium Americas Corp", "Carnival Corporation"],
        "transport": ["Tesla", "Southwest Airlines", "J.B. Hunt Transport Services", "United Parcel Service", "CSX Corporation",
                      "FedEx"],
        "energy": ["Enphase Energy", "First Solar", "Freeport-McMoRan", "ConocoPhillips", "Exxon Mobil",
                   "Pioneer Natural Resources"],
        "health": ["Amgen", "Gilead Sciences", "Moderna", "Intuitive Surgical", "Regeneron Pharmaceuticals",
                   "Illumina"],
        "technology": ["Apple", "Google", "Microsoft", "NVIDIA", "Meta", "Adobe"]
    }

    # Loop through sectors and companies
    for sector, companies in sectors_full_name.items():
        result[sector] = {}

        # Loop through each company in the sector with its full name
        for i, company_name in enumerate(companies):
            company_key = f"company_{i}"

            # Find the corresponding symbol for the company (assuming the symbol is in the 'sectors' dict)
            symbol = None
            # Iterate over all sectors and their respective companies
            for sec, syms in sectors.items():
                # Check if the full company name matches any of the names in the sector's company list
                if company_name in [get_full_company_name(comp) for comp in syms]:
                    # Find the corresponding symbol for the company name
                    symbol = next(comp for comp in syms if company_name == get_full_company_name(comp))
                    break  # Stop once we find the matching company

            # If no symbol found, skip the company
            if symbol is None:
                print(f"Symbol not found for {company_name}. Skipping.")
                continue

            # Fetch the current price for the company
            current_price = get_candle_average_price(symbol, exchange, interval, 0, type)
            if current_price is None:
                print(f"Could not fetch current price for {company_name} ({symbol}). Skipping.")
                continue

            result[sector][company_key] = {
                "company_name": company_name,
                "symbol": symbol,
                "current_price": current_price,
                "average_prices": {}
            }

            # Fetch average prices for this company over 30 backtrack periods
            for backtrack in range(30):
                avg_price = get_candle_average_price(symbol, exchange, interval, backtrack, type)
                if avg_price is not None:
                    result[sector][company_key]["average_prices"][f"backtrack_{backtrack}"] = avg_price

    return result



def display_result(result):
    """
    Displays the result dictionary for verification.

    Parameters:
    - result: The result dictionary to display.
    """
    # Print the result as a pretty-printed JSON string
    print(json.dumps(result, indent=4, sort_keys=True))

def main():
    symbol = input("Enter the stock symbol: ").upper()
    sector = get_sector(symbol)
    if not sector:
        print(f"Error: Symbol {symbol} not found in any sector.")
        return

    print(f"Symbol {symbol} is in the {sector} sector.")

    exchange = "stocks"
    interval = "1w"
    type = "stocks"

    # Fetch current price for the input symbol
    current_price = get_candle_average_price(symbol, exchange, interval, 0, type)
    if current_price is not None:
        print(f"Current Price for {symbol}: {current_price}")

    # # Loop through backtrack from 0 to 29 and fetch average prices
    # for backtrack in range(30):
    #     avg_price = get_candle_average_price(symbol, exchange, interval, backtrack, type)
    #     if avg_price is not None:
    #         print(f"Average Price for {symbol} with backtrack {backtrack}: {avg_price}")

    # Build and display the result dictionary
    result = build_result()
    display_result(result)


if __name__ == "__main__":
    main()
