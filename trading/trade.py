import alpaca_trade_api as tradeapi
import yfinance as yf
import requests
import json
import time

# Alpaca API credentials
API_KEY = 'PKQJHJIPU1WQ92N4UO30'
API_SECRET = 'TCi4S4dhaSJZe62CdbrcxPHWYpTYgWaXyQlfzany'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use Alpaca's paper trading API

# Alpaca API setup
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# URL of the prediction server (app.js)
PREDICTION_SERVER_URL = "http://localhost:3000/predict"

# Function to fetch current stock data from Yahoo Finance
def get_current_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d", interval="1m")  # Fetch 1-minute intervals of today's data
    if len(hist) == 0:
        raise ValueError(f"No data found for symbol {symbol}")

    # Select features
    latest_data = hist.iloc[-1]  # Get the last available row of data

    # Ensure to create a list with exactly 10 features
    selected_features = [
        latest_data['Open'],  # Open price
        latest_data['High'],  # High price
        latest_data['Low'],   # Low price
        latest_data['Close'],  # Close price
        latest_data['Volume'],  # Volume
        hist['Close'].iloc[-2],  # Previous close price
        (latest_data['High'] + latest_data['Low']) / 2,  # Average price
        (latest_data['Close'] - latest_data['Open']) / latest_data['Open'],  # Price change percentage
        hist['Close'].rolling(window=5).mean().iloc[-1],  # 5-period moving average
        hist['Close'].rolling(window=10).mean().iloc[-1],  # 10-period moving average
    ]

    return selected_features[:10]  # Ensure you return exactly 10 features

# Function to get prediction from the TensorFlow.js server
def get_prediction(stock_data):
    # Prepare data for the request (expected to be a JSON)
    payload = {"inputData": stock_data}  # Expecting a list of 10 features

    # Send POST request to the app.js server
    response = requests.post(PREDICTION_SERVER_URL, json=payload)

    if response.status_code == 200:
        prediction = response.json().get('prediction')
        return prediction
    else:
        raise Exception(f"Prediction request failed with status code {response.status_code}")

def buy(symbol,qty):
    api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
    )

def sell(symbol,qty):
    api.submit_order(
            symbol=symbol,
            qty=qty,
            side='sell',
            type='market',
            time_in_force='gtc'
    )

# Function to make a trading decision (buy or sell) based on the prediction
def make_trade_decision(prediction, position):
    symbol = 'AMD'
    if prediction is None:
        print("Prediction is None. Cannot make trade decision.")
        return position  # Return the current position without making changes

    if prediction > 0:
        print("Prediction is positive: Buy")
        if position == 0:
            buy(symbol, 1)
        elif position == -1:
            buy(symbol, 2)
        return 1
    else:
        print("Prediction is negative: Sell")
        if position == 0:
            sell(symbol, 1)
        elif position == 1:
            sell(symbol, 2)
        return -1

if __name__ == "__main__":
    symbol = 'AMD'  # You can change this to the stock symbol you want to trade
    position = 0

    try:
        while True:
            # Step 1: Get current stock data
            current_data = get_current_stock_data(symbol)
            print(f"Current stock data for {symbol}: {current_data}")

            # Step 2: Get prediction from the app.js server
            prediction = get_prediction(current_data)
            print(f"Prediction for {symbol}: {prediction}")

            # Step 3: Make a trade decision based on the prediction
            posistion = make_trade_decision(prediction,position)

            # Sleep for 60 seconds before fetching data again (you can adjust this)
            time.sleep(60)

    except Exception as e:
        print(f"Error: {e}")
