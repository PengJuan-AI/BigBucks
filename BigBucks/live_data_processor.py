import sqlite3
import os
import urllib.request
import json
import yfinance as yf
from datetime import datetime, timedelta
from yahoo_fin import stock_info as si
from urllib.parse import quote
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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
        c.execute("INSERT OR REPLACE INTO Assets_data (assetid, history_date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (assetid, row[0], row[1], row[2], row[3], row[4], row[5], int(row[6])))
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
    live_price = round(si.get_live_price(symbol),2)
    return live_price

# Store historical data into database
def store_stock_data(symbol):
    # Open database connection
    db_path = os.path.join(os.path.dirname(__file__), 'BigBucks.db')
    conn = sqlite3.connect(db_path)

    # Add asset to Assets_info table and get its assetid
    assetid, company_name, shares_outstanding = add_asset(conn, symbol)

    # Set the end date as the current date
    end_date = datetime.today().strftime('%Y-%m-%d')
    # Set the start date as five years before the end date
    start_date = (datetime.today() - timedelta(days=365*5)).strftime('%Y-%m-%d')

    # Get historical data from Yahoo Finance
    data = yf.download(symbol, start=start_date, end=end_date)
    # Select and reorder columns
    data = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    data.reset_index(inplace=True)
    data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    data.rename(columns={'Date': 'history_date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close', 'Volume': 'volume'}, inplace=True)
    # Convert date format to match SQLite
    data['history_date'] = data['history_date'].dt.strftime('%Y-%m-%d')
    stock_data = [tuple(x) for x in data.to_records(index=False)]
    
    # Add stock data to Assets_data table
    add_stock_data(conn, assetid, stock_data)

    # Close database connection
    conn.close()


def get_symbol_by_name(company_name):
    # construct the URL to retrieve the stock symbol for the given company name
    encoded_company_name = quote(company_name)
    url = f'https://query2.finance.yahoo.com/v1/finance/search?q={encoded_company_name}&quotesCount=1&newsCount=0'

    # send an HTTP GET request to the URL and retrieve the response content
    response = urllib.request.urlopen(url)
    content = response.read()

    # parse the response content from JSON format into a Python dictionary
    data = json.loads(content.decode('utf8'))

    # extract the stock symbol from the data dictionary and return it
    return data['quotes'][0]['symbol']

def get_live_price_by_name(company_name):
    symbol = get_symbol_by_name(company_name)
    live_price = get_live_price(symbol)
    return live_price


def get_company_shares_by_name(company_name):
    symbol = get_symbol_by_name(company_name)
    shares_outstanding = get_company_shares(symbol)
    return shares_outstanding


'''
#test
symbols = ['AAPL', 'MSFT']
for symbol in symbols:
    store_stock_data(symbol)
    live_price = get_live_price(symbol)
    print(live_price)

company_name = 'microsof'
s = get_company_shares_by_name(company_name)
p = get_live_price_by_name(company_name)
b = get_symbol_by_name(company_name)
print(s)
print(p)
print(b)   
'''