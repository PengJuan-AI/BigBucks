import sqlite3
import os
import urllib.request
import json
import yfinance as yf
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si

# Add asset to Assets_info table and get its assetid
def add_asset(conn, symbol):
    c = conn.cursor()
    # Check if asset already exists in table
    c.execute("SELECT assetid, name, shares FROM Assets_info WHERE symbol=?", (symbol,))
    asset = c.fetchone()
    if asset is not None:
        assetid, company_name, shares = asset
        # Update shares if asset already exists
        shares_outstanding = get_company_shares(symbol)
        c.execute("UPDATE Assets_info SET shares=? WHERE assetid=?", (shares_outstanding, assetid))
        conn.commit()
        return assetid, company_name, shares_outstanding
    # If asset doesn't exist, get company name and shares from Yahoo Finance and insert into table
    company_name = get_company_name(symbol)
    shares_outstanding = get_company_shares(symbol)
    c.execute("INSERT INTO Assets_info (symbol, name, shares) VALUES (?, ?, ?)", (symbol, company_name, shares_outstanding))
    assetid = c.lastrowid
    conn.commit()
    return assetid, company_name, shares_outstanding

# Add stock data to Assets_data table
def add_stock_data(conn, assetid, stock_data):
    c = conn.cursor()
    for row in stock_data:
        c.execute("INSERT OR REPLACE INTO Assets_data (assetid, date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (assetid, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    conn.commit()

# Get company's name by its symbol from Yahoo Finance
def get_company_name(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    company_name = json.loads(content.decode('utf8'))['quotes'][0]['shortname']
    return company_name

# Get company's outstanding shares by its symbol from Yahoo Finance
def get_company_shares(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile,defaultKeyStatistics,financialData')
    content = response.read()
    data = json.loads(content.decode('utf8'))
    shares_outstanding = data['quoteSummary']['result'][0]['defaultKeyStatistics']['sharesOutstanding']['raw']
    return shares_outstanding

# Get live price of a stock by its symbol from Yahoo Finance
def get_live_price(symbol):
    live_price = si.get_live_price(symbol)
    return live_price

# Open database connection
db_path = os.path.join(os.path.dirname(__file__), '2.db')
conn = sqlite3.connect(db_path)

# Process each stock symbol
symbols = ['AAPL','MSFT']
for symbol in symbols:
    assetid, company_name, shares_outstanding = add_asset(conn, symbol)
    # Set the end date as the current date
    end_date = datetime.today().strftime('%Y-%m-%d')
    # Set the start date as one year before the end date
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    # Get live data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)
    # Select and reorder columns
    data = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    data.reset_index(inplace=True)
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    data.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
    # Convert date format to match SQLite
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')
    stock_data = [tuple(x) for x in data.to_records(index=False)]
    
    live_price = get_live_price(symbol)
    print(live_price)
    # Add stock data to Assets_data table
    #print(stock_data)
    add_stock_data(conn, assetid, stock_data)

# Close database connection
conn.close()
