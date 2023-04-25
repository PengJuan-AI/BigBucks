import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
from BigBucks.analysis import get_hist_data
from Packages.live_data_processor import get_live_price_by_input

date = '2023-4-24'

def test_single_asset(client, auth, app):
    auth.login()
    symbol = 'AAPL'
    price = get_live_price_by_input(symbol,date)

    with app.app_context():
        client.post('/order/buy',
                    data={'symbol': symbol, 'date': date, 'price': price, 'share': 100, 'action': 'buy'})
        
        response =  client.get('analysis/single')

        assert response.status_code == 200
        assert b'AAPL' in response.data

def test_multiple_asset(client, auth, app):
    auth.login()
    symbols = ['AAPL', 'TSLA', 'MSFT', 'GM']

    with app.app_context():
        for s in symbols:
            response = client.post('/order/buy',
                                   data={'symbol': s, 'date': date, 'price': get_live_price_by_input(s, date),'share': 200, 'action': 'buy'})

        response = client.get('analysis/multiple')

        assert response.status_code == 200
        assert b'AAPL' in response.data and b'TSLA' in response.data and b'MSFT' in response.data and b'GM' in response.data