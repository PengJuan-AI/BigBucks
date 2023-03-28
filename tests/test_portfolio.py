import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
from BigBucks.analysis import get_hist_data
from live_data_processor import get_live_price

def test_get_hist_data(client, auth, app):
    auth.login()
    symbol = 'AAPL'
    price = get_live_price(symbol)

    with app.app_context():
        client.post('/order/buy',
                    data={'symbol': symbol, 'date': '2023-3-27', 'price': price, 'share': 100, 'action': 'buy'})
        
        response =  client.post('analysis/portfolio/AAPL') 
        print(response.data)

        assert response.status_code == 200
        assert b'{"date"' in response.data
