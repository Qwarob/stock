# Stock Trading Project

This project uses TensorFlow.js to predict stock prices and Alpaca API for trading.

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd stock_trading_project
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   npm install
   python trading/data_fetch.py
   node server/model.js
   npm start

   bash
   source venv/bin/activate
   python trading/trade.py