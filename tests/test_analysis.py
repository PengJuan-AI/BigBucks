import pytest
from flask import g, session
from BigBucks.db import get_db
# from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
import numpy as np
from Packages.live_data_processor import get_live_price_by_input
from BigBucks.Packages.get_weights import get_portfolio_weights
from Packages.efficient_frontier import cal_returns,cal_returns_with_date,get_ef,get_port_info

date = '2023-4-24'

def test_get_weights(client, app, auth):
    auth.login()
    with app.app_context():
        db = get_db()
        price1 = get_live_price_by_input('AAPL', date)
        price2 = get_live_price_by_input('TSLA', date)
        client.post('/order/buy',
                    data={'symbol': 'AAPL', 'date': date, 'price': price1, 'share': 200, 'action': 'buy'})
        client.post('/order/buy',
                    data={'symbol': 'TSLA', 'date': date, 'price': price2, 'share': 200, 'action': 'buy'})
        total_value = price1*200+price2*200
        portfolio = db.execute("SELECT * FROM portfolio where userid=1").fetchall()
        weights = get_portfolio_weights(1)
        assert portfolio[0]['symbol'] == 'AAPL'
        assert weights['AAPL'] == round(price1*200/total_value,2)
        assert weights['AAPL']+weights['TSLA'] == 1

def test_ef_bp(auth, client, app):
    auth.login()
    with app.app_context():
        response = client.get('analysis/ef')
        assert b'Please add asset into your portfolio.' in response.data
        assert response.status_code == 200

def test_ef(auth, client, app):
    auth.login()
    symbols = ['AAPL', 'TSLA', 'MSFT', 'GM']

    with app.app_context():
        for s in symbols:
            response = client.post('/order/buy',
                        data={'symbol': s, 'date': date, 'price': get_live_price_by_input(s,date), 'share': 200,
                              'action': 'buy'})
        port = get_portfolio_weights(1)
        W,risk_return = get_ef(port)

        assert W is not None
        assert len(risk_return) == 100
