import http.client
import json
from pprint import pprint

# Token for API authentication
token = "API_KEY"

company_data = {
    "sectors": {
        "technology": [
            {"symbol": "AAPL", "name": "Apple"},
            {"symbol": "GOOGL", "name": "Google"},
            {"symbol": "MSFT", "name": "Microsoft"},
            {"symbol": "NVDA", "name": "NVIDIA"},
            {"symbol": "META", "name": "Meta"},
            {"symbol": "AMD", "name": "Advanced Micro Devices Inc"}
        ],
        "health": [
            {"symbol": "AMGN", "name": "Amgen"},
            {"symbol": "GILD", "name": "Gilead Sciences"},
            {"symbol": "MRNA", "name": "Moderna"},
            {"symbol": "ISRG", "name": "Intuitive Surgical"},
            {"symbol": "REGN", "name": "Regeneron Pharmaceuticals"},
            {"symbol": "ILMN", "name": "Illumina"}
        ],
        "energy": [
            {"symbol": "ENPH", "name": "Enphase Energy"},
            {"symbol": "FSLR", "name": "First Solar"},
            {"symbol": "FCX", "name": "Freeport-McMoRan"},
            {"symbol": "COP", "name": "ConocoPhillips"},
            {"symbol": "XOM", "name": "Exxon Mobil"},
            {"symbol": "OXY", "name": "Occidental Petroleum Corp"}
        ],
        "raw_materials": [
            {"symbol": "FCX", "name": "Freeport-McMoRan"},
            {"symbol": "NEM", "name": "Newmont Mining"},
            {"symbol": "NUE", "name": "Nucor"},
            {"symbol": "ALB", "name": "Albemarle"},
            {"symbol": "CF", "name": "CF Industries Holdings, Inc"},
            {"symbol": "CCL", "name": "Carnival Corporation"}
        ],
        "transport": [
            {"symbol": "TSLA", "name": "Tesla"},
            {"symbol": "LUV", "name": "Southwest Airlines"},
            {"symbol": "JBHT", "name": "J.B. Hunt Transport Services"},
            {"symbol": "UPS", "name": "United Parcel Service"},
            {"symbol": "CSX", "name": "CSX Corporation"},
            {"symbol": "FDX", "name": "FedEx"}
        ],
        "manufacturing": [
            {"symbol": "AMAT", "name": "Applied Materials"},
            {"symbol": "TXN", "name": "Texas Instruments"},
            {"symbol": "HON", "name": "Honeywell"},
            {"symbol": "INTC", "name": "Intel"},
            {"symbol": "ADI", "name": "Analog Devices"},
            {"symbol": "LRCX", "name": "Lam Research"}
        ],
        "services": [
            {"symbol": "AMZN", "name": "Amazon"},
            {"symbol": "BKNG", "name": "Booking Holdings"},
            {"symbol": "SBUX", "name": "Starbucks"},
            {"symbol": "COST", "name": "Costco"},
            {"symbol": "EBAY", "name": "eBay"},
            {"symbol": "MAR", "name": "Marriott"}
        ]
    }
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
    Determines the sector for a given symbol using the new `company_data` structure.

    Parameters:
    - symbol: The stock symbol to check.

    Returns:
    - The sector to which the symbol belongs, or None if the symbol is not found.
    """
    # Iterate through each sector in the company_data
    for sector, companies in company_data["sectors"].items():
        # Iterate through companies in the sector
        for company in companies:
            if company["symbol"] == symbol:
                return sector
    return None

def build_result():
    """
    Builds a nested result dictionary with sectors and company data based on the new company_data structure.

    Returns:
    - A dictionary containing sector names as keys and their corresponding companies' details.
    """
    result = {}
    exchange = "stocks"  # Assuming all are stock exchanges
    interval = "1w"  # Weekly interval
    type = "stocks"  # Stock type

    # Loop through each sector and its companies in the new company_data structure
    for sector, companies in company_data["sectors"].items():
        result[sector] = {}

        # Loop through each company in the sector
        for i, company in enumerate(companies):
            company_key = f"company_{i}"

            symbol = company["symbol"]
            company_name = company["name"]

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
    vals = {"result": result}
    return vals

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

    # Build and display the result dictionary
    result = build_result()
    display_result(result)

if __name__ == "__main__":
    main()
