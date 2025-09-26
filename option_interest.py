
import json
import logging
from logging.handlers import RotatingFileHandler
import configparser
from rauth import OAuth1Service
import webbrowser

# logger settings
logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("python_client.log", maxBytes=5 * 1024 * 1024, backupCount=3)
FORMAT = "%(asctime)-15s %(message)s"
fmt = logging.Formatter(FORMAT, datefmt='%m/%d/%Y %I:%M:%S %p')
handler.setFormatter(fmt)
logger.addHandler(handler)

def get_option_interest(session, base_url, symbol, expiry_year, expiry_month, expiry_day, strike_price, option_type):
    """
    Fetches the open interest for a specific option contract.

    :param session: authenticated session
    :param base_url: The base URL for the E*TRADE API.
    :param symbol: The underlying stock symbol (e.g., "AAPL").
    :param expiry_year: The four-digit expiration year (e.g., 2025).
    :param expiry_month: The two-digit expiration month (e.g., "01").
    :param expiry_day: The two-digit expiration day (e.g., "20").
    :param strike_price: The strike price of the option.
    :param option_type: "CALL" or "PUT".
    :return: The open interest as an integer, or None if not found.
    """

    option_symbol = f"{symbol}:{expiry_year}:{expiry_month}:{expiry_day}:{option_type}:{strike_price}"
    url = f"{base_url}/v1/market/quote/{option_symbol}.json"
    params = {"detailFlag": "OPTIONS"}

    response = session.get(url, params=params)
    logger.debug("Request Header: %s", response.request.headers)

    if response is not None and response.status_code == 200:
        parsed = json.loads(response.text)
        logger.debug("Response Body: %s", json.dumps(parsed, indent=4, sort_keys=True))

        data = response.json()
        if data is not None and "QuoteResponse" in data and "QuoteData" in data["QuoteResponse"]:
            for quote in data["QuoteResponse"]["QuoteData"]:
                if quote is not None and "Option" in quote and "openInterest" in quote["Option"]:
                    return quote["Option"]["openInterest"]
    else:
        logger.error(f"Error fetching option interest for {option_symbol}: {response.text}")

    return None

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    etrade = OAuth1Service(
        name="etrade",
        consumer_key=config["DEFAULT"]["CONSUMER_KEY"],
        consumer_secret=config["DEFAULT"]["CONSUMER_SECRET"],
        request_token_url="https://api.etrade.com/oauth/request_token",
        access_token_url="https://api.etrade.com/oauth/access_token",
        authorize_url="https://us.etrade.com/e/t/etws/authorize?key={}&token={}",
        base_url="https://api.etrade.com")

    base_url = config["DEFAULT"]["PROD_BASE_URL"]

    # Step 1: Get OAuth 1 request token and secret
    request_token, request_token_secret = etrade.get_request_token(
        params={"oauth_callback": "oob", "format": "json"})

    # Step 2: Go through the authentication flow. Login to E*TRADE.
    authorize_url = etrade.authorize_url.format(etrade.consumer_key, request_token)
    webbrowser.open(authorize_url)
    text_code = input("Please accept agreement and enter verification code from browser: ")

    # Step 3: Exchange the authorized request token for an authenticated OAuth 1 session
    session = etrade.get_auth_session(request_token,
                                  request_token_secret,
                                  params={"oauth_verifier": text_code})

    # Get user input
    symbol = input("Enter underlying symbol (e.g., AAPL): ").upper().strip()
    expiry_year = input("Enter expiration year (YYYY): ").strip()
    expiry_month = input("Enter expiration month (MM): ").strip()
    expiry_day = input("Enter expiration day (DD): ").strip()
    strike_price = float(input("Enter strike price: ").strip())
    option_type = input("Enter option type (CALL or PUT): ").upper().strip()

    open_interest = get_option_interest(session, base_url, symbol, expiry_year, expiry_month, expiry_day, strike_price, option_type)

    if open_interest is not None:
        print(f"Open Interest: {open_interest}")
    else:
        print("Could not retrieve open interest.")
