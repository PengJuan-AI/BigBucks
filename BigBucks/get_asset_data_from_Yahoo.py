import csv
import sqlite3
import os
import urllib.request
# from urllib import urlopen
import ssl
import json

# Get company's name by its symbol from Yahoo Finance
def get_company_name(symbol):
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={symbol}',context=context)

    content = response.read()
    company_name = json.loads(content.decode('utf8'))['quotes'][0]['shortname']
    return company_name

# if __name__ == '__main__':
#     name = get_company_name('AAPL')
#     print("Stock name:", name)
