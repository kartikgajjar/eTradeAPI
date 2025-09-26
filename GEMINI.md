# Project Overview

This project is a Python script that fetches the open interest for a specific option contract from the E*TRADE API. It uses OAuth 1.0a for authentication and is designed to be run from the command line.

## Key Technologies

*   Python 3
*   `rauth` library for OAuth 1.0a authentication
*   `configparser` for managing API credentials

# Building and Running

## 1. Installation

Install the necessary Python libraries using pip:

```bash
pip install -r requirements.txt
```

## 2. Configuration

The `config.ini` file stores the E*TRADE API credentials. You will need to replace the placeholder values with your own API key and secret.

```ini
[DEFAULT]
CONSUMER_KEY = your_consumer_key
CONSUMER_SECRET = your_consumer_secret
SANDBOX_BASE_URL=https://apisb.etrade.com
PROD_BASE_URL=https://api.etrade.com
```

## 3. Running the Script

Execute the script from your terminal:

```bash
python option_interest.py
```

The script will guide you through the E*TRADE authentication process, which involves opening a URL in your web browser and entering a verification code. After authentication, it will prompt you for the following option details:

*   Underlying symbol (e.g., AAPL)
*   Expiration year (YYYY)
*   Expiration month (MM)
*   Expiration day (DD)
*   Strike price
*   Option type (CALL or PUT)

The script will then output the open interest for the specified option contract.

# Development Conventions

*   **Authentication:** The script uses the `rauth` library to handle the OAuth 1.0a authentication flow with E*TRADE.
*   **Configuration:** API keys and endpoints are stored in `config.ini` and loaded using the `configparser` library.
*   **Logging:** The script includes basic logging to a file named `python_client.log`.
*   **User Interaction:** The script is interactive, prompting the user for input to specify the desired option contract.
