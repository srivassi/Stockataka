import http.client
import json

# Sectors
services = ["AMZN", "COST", "SBUX", "BKNG", "MAR", "ABNB"]
manufacturing = ["HON", "AMAT", "INTC", "MU", "AMD", "TSLA"]
aviation = ["AAL", "ALGT", "LUV", "ALK", "SKYW", "HA"]
transport = ["TSLA", "PCAR", "KNX", "CAR", "EXPD", "JBHT"]
energy = ["ENPH", "SPWR", "CLNE", "FSLR", "PLUG", "FCEL"]
health = ["WBA", "MRNA", "ISRG", "AMGN", "REGN", "GILD"]
technology = ["AAPL", "GOOGL", "MSFT", "NVDA", "META", "INTC"]

# Function to check which sector the symbol belongs to
def get_sector(symbol):
    # Check which sector the symbol belongs to
    if symbol in services:
        return "services"
    elif symbol in manufacturing:
        return "manufacturing"
    elif symbol in aviation:
        return "aviation"
    elif symbol in transport:
        return "transport"
    elif symbol in energy:
        return "energy"
    elif symbol in health:
        return "health"
    elif symbol in technology:
        return "technology"
    else:
        return None

def get_candle_roc(symbol, exchange, interval, backtrack, type):
    """
    Fetches the Rate of Change (ROC) for a given symbol directly from the taapi.p.sulu.sh API.

    Parameters:
    - symbol: Trading pair symbol (e.g., "BTC/USDT").
    - exchange: Exchange name (e.g., "binance").
    - interval: Time interval per candle (e.g., "1w" for weekly).
    - backtrack: Number of historical candles to fetch (how many weeks back).

    Prints:
    - The ROC for the symbol for the given interval and backtrack.
    """
    conn = http.client.HTTPSConnection("taapi.p.sulu.sh")

    headers = {
        'Accept': "application/json",
        'Authorization': "Bearer sk_live_KLTxJeItYDWnMh8tiyDEXHMVti9gSNto"
    }

    # Define path with parameters for the ROC endpoint
    path = f"/roc?exchange={exchange}&symbol={symbol}&interval={interval}&backtrack={backtrack}&type={type}"

    # Send request and process response
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()

    # Check if the response is successful
    if res.status == 200:
        res_data = res.read().decode("utf-8")
        # Debugging: Print raw response
        #print(f"Response Data for {symbol} with backtrack={backtrack}: {res_data}")

        try:
            data = json.loads(res_data)

            # Check if the 'value' key is present in the response
            if 'value' in data:
                print(f"Rate of Change for {symbol} with backtrack {backtrack}: {data['value']}%")
            else:
                print(f"Error: 'value' key missing in the response for backtrack={backtrack}.")
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON response.")
    else:
        print(f"Error: {res.status} {res.reason}")

# Main function to get the symbol and fetch candles
def main():
    # Input the stock symbol
    symbol = input("Enter the stock symbol: ").upper()  # Ensures the symbol is uppercase

    # Get sector and validate symbol
    sector = get_sector(symbol)
    if not sector:
        print(f"Error: Symbol {symbol} not found in any sector.")
        return

    print(f"Symbol {symbol} is in the {sector} sector.")

    # Define the exchange and interval
    exchange = "stocks"  # Assuming stocks exchange for all, change as necessary
    interval = "1w"  # Weekly interval
    type = "stocks"

    # Loop through backtrack from 1 to 10
    for backtrack in range(1, 11):
        get_candle_roc(symbol, exchange, interval, backtrack, type)

# Run the main function
main()

