import yfinance as yf
import pandas as pd

def get_historical_data(symbol, start, end):
    # Fetch historical data from Yahoo Finance
    stock_data = yf.download(symbol, start=start, end=end)
    
    # Select and calculate features
    stock_data['Prev Close'] = stock_data['Close'].shift(1)  # Previous close price
    stock_data['Price Change %'] = (stock_data['Close'] - stock_data['Open']) / stock_data['Open']  # Price change percentage
    stock_data['Avg Price'] = (stock_data['High'] + stock_data['Low']) / 2  # Average price
    stock_data['5-MA'] = stock_data['Close'].rolling(window=5).mean()  # 5-period moving average
    stock_data['10-MA'] = stock_data['Close'].rolling(window=10).mean()  # 10-period moving average

    # Keep only necessary columns and drop rows with NaN values
    features = stock_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Prev Close', 'Avg Price', 'Price Change %', '5-MA', '10-MA']].dropna()
    
    return features.reset_index()

if __name__ == "__main__":
    # Fetch historical data for AMD
    historical_data = get_historical_data('AMD', '2023-01-01', '2024-01-01')
    historical_data.to_csv('data/historical_data.csv', index=False)
    print(historical_data)
