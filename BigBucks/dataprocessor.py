import csv
import sqlite3
import os
import yfinance as yf
import requests
import json

def read_stock_data(filename):
    with open('static/stockdata/' + filename, 'r') as f:
        reader = csv.reader(f)
        # Skip header row
        next(reader)
        # Get data
        data = [(row[0], float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]), int(row[6])) for row in reader]
    return data

#data = read_stock_data('AAPL.csv')
#print(data)

# Add asset to Assets_info table and get its assetid
def add_asset(conn, symbol, name):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO Assets_info (symbol, name) VALUES (?, ?)", (symbol, name))
    conn.commit()
    c.execute("SELECT assetid FROM Assets_info WHERE symbol=?", (symbol,))
    assetid = c.fetchone()[0]
    return assetid

# Add stock data to Assets_data table
def add_stock_data(conn, assetid, stock_data):
    c = conn.cursor()
    for row in stock_data:
        c.execute("INSERT OR REPLACE INTO Assets_data (assetid, date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (assetid, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    conn.commit()

# Open database connection
db_path = os.path.join(os.path.dirname(__file__), 'BigBucks.db')
conn = sqlite3.connect(db_path)

# Process each CSV file in the stockdata directory
for filename in os.listdir('static/stockdata'):
    if not filename.endswith('.csv'):
        continue
    symbol = filename[:-4]  # Remove '.csv' extension
    stock_data = read_stock_data(filename)
     
    '''    
    ticker = yf.Ticker(symbol) # Get company name by its stock symbol
    company_name = ticker.info["longName"]
    assetid = add_asset(conn, symbol, company_name)
    '''

    assetid = add_asset(conn, symbol, 'company_name')
    add_stock_data(conn, assetid, stock_data)

# Close database connection
conn.close()
