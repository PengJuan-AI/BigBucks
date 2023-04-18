import pytest
from flask import g, session
from BigBucks.db import get_db
# from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares
import numpy as np
from Packages.live_data_processor import get_live_price
from BigBucks.Packages.get_weights import get_portfolio_weights
from Packages.efficient_frontier import cal_returns,cal_returns_with_date,get_ef,cal_port_return,cal_port_volatility

# def test_get_weights(client, app, auth):
#     auth.login()
#
#     with app.app_context():
#         price1 = get_live_price('AAPL')
#         price2 = get_live_price('TSLA')
#         client.post('/order/buy',
#                     data={'symbol': 'AAPL', 'date': '2023-3-15', 'price': price1, 'share': 200, 'action': 'buy'})
#         client.post('/order/buy',
#                     data={'symbol': 'TSLA', 'date': '2023-3-15', 'price': price2, 'share': 200, 'action': 'buy'})
#         total_value = price1*200+price2*200
#         weights = get_portfolio_weights(1)
#         assert weights['AAPL'] == round(price1*200/total_value,2)
#         assert weights['AAPL']+weights['TSLA'] == 1

# def test_return_volatility(client, app, auth):
#     auth.login()
#     symbols = ['AAPL', 'TSLA']
#
#     with app.app_context():
#         for s in symbols:
#             client.post('/order/buy',
#                 data={'symbol': s, 'date': '2023-3-27', 'price': get_live_price(s), 'share': 200, 'action': 'buy'})
#
#         for s in symbols:
#             assert cal_returns(s) is not None
            
# def test_ef(auth, client, app):
#     auth.login()
#     symbols = ['AAPL', 'TSLA', 'MSFT', 'GM']
#
#     with app.app_context():
#         for s in symbols:
#             response = client.post('/order/buy',
#                         data={'symbol': s, 'date': '2023-3-27', 'price': get_live_price(s), 'share': 200,
#                               'action': 'buy'})
#         port = get_portfolio_weights(1)
#         W,risk_return = get_ef(port)
#
#         assert W is not None
#         assert len(risk_return) == 100
#         # assert np.amax(R) < 1

def test_ef_bp(auth, client, app):
    auth.login()
    symbols = ['AAPL', 'TSLA', 'MSFT', 'GM']

    with app.app_context():
        for s in symbols:
            client.post('/order/buy',
                                   data={'symbol': s, 'date': '2023-3-27', 'price': get_live_price(s), 'share': 200,'action': 'buy'})

        assert client.get('analysis/ef').status_code == 200

def test_multiple(auth, client, app):
    auth.login()
    symbols = ['AAPL', 'TSLA']

    with app.app_context():
        for s in symbols:
            cal_returns_with_date(s)
        #     client.post('/order/buy',
        #                 data={'symbol': s, 'date': '2023-3-27', 'price': get_live_price(s), 'share': 200,
        #                       'action': 'buy'})

