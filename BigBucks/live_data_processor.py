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


# Get company's name by its symbol from Yahoo Finance
def get_company_name(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}')
    content = response.read()
    data = json.loads(content.decode('utf8')) 
    if 'shortname' in data['quotes'][0]:
        company_name = data['quotes'][0]['shortname']
        return company_name
    else:
        return None

# Get company's outstanding shares by its symbol from Yahoo Finance
def get_company_shares(symbol):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile,defaultKeyStatistics,financialData')
    content = response.read()
    data = json.loads(content.decode('utf8'))
    if 'sharesOutstanding' in data['quoteSummary']['result'][0]['defaultKeyStatistics']:
        shares_outstanding = data['quoteSummary']['result'][0]['defaultKeyStatistics']['sharesOutstanding']['raw']
        return shares_outstanding
    else:
        return None

# Get live price of a stock by its symbol from Yahoo Finance
def get_live_price(symbol):
    live_price = round(si.get_live_price(symbol),2)
    return live_price

# Store historical data into database
def store_historical_data(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    stock_data = yf.download(symbol, start=start_date, end=end_date)

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'BigBucks.db'))
    conn = sqlite3.connect(db_path)
    
    c = conn.cursor()

    for index, row in stock_data.iterrows():
        symbol = symbol
        history_date = index.strftime('%Y-%m-%d')
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        adj_close_price = row['Adj Close']
        volume = row['Volume']

        c.execute("INSERT OR REPLACE INTO Assets_data (symbol, history_date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (symbol, history_date, open_price, high_price, low_price, close_price, adj_close_price, volume))

    conn.commit()
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

def store_data_by_name(company_name):
    symbol = get_symbol_by_name(company_name)
    store_historical_data(symbol)

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
store_data_by_name(company_name)
print(s)
print(p)
print(b)
'''
