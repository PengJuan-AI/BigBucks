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
    live_price = float("{:.2f}".format(round(si.get_live_price(symbol),2)))
    return live_price

# Get the sector of a company by its symbol from Yahoo Finance
def get_company_sector(symbol):
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    if 'quoteSummary' in data and 'result' in data['quoteSummary'] and \
            data['quoteSummary']['result'][0]['assetProfile'] and 'sector' in data['quoteSummary']['result'][0]['assetProfile']:
        sector = data['quoteSummary']['result'][0]['assetProfile']['sector']
        return sector
    else:
        return None

# Get the industry of a company by its symbol from Yahoo Finance    
def get_company_industry(symbol):
    url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules=assetProfile"
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
    if 'quoteSummary' in data and 'result' in data['quoteSummary'] and \
            data['quoteSummary']['result'][0]['assetProfile'] and 'industry' in data['quoteSummary']['result'][0]['assetProfile']:
        industry = data['quoteSummary']['result'][0]['assetProfile']['industry']
        return industry
    else:
        return None

# Store historical data into database
def get_historical_data(symbol):
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    # db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'BigBucks.db'))
    # conn = sqlite3.connect(db_path)
    #
    # c = conn.cursor()
        # c.execute("INSERT OR REPLACE INTO Assets_data (symbol, history_date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (symbol, history_date, open_price, high_price, low_price, close_price, adj_close_price, volume))
    # conn.commit()
    # conn.close()

    return stock_data

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

def get_live_price_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        live_price = get_live_price(symbol)
        return live_price
    else:
        live_price = get_live_price(input)
        return live_price

def get_company_shares_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        shares_outstanding = get_company_shares(symbol)
        return shares_outstanding
    else:
        shares_outstanding = get_company_shares(input)
        return shares_outstanding

def get_data_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        stock_data = get_historical_data(symbol)
        return stock_data
    else:
        stock_data = get_historical_data(input)
        return stock_data

def get_sector_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        sector = get_company_sector(symbol)
        return sector
    else:
        sector = get_company_sector(input)
        return sector

def get_industry_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        industry = get_company_industry(symbol)
        return industry
    else:
        industry = get_company_industry(input)
        return industry

def get_name_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        name = get_company_name(symbol)
        return name
    else:
        name = get_company_name(input)
        return name

def get_symbol_by_input(input):
    if input.isalpha():
        symbol = get_symbol_by_name(input)
        return symbol
    else:
        return input
    
'''
a = get_name_by_input('msft')
b = get_symbol_by_input('micros')
c = get_symbol_by_input('msft')
print(a)
print(b)
print(c)
'''