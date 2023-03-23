import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance,get_assetid, buy_asset, get_company_name,get_company_shares

def test_buy(client, auth,app):
    auth.login()
    assert client.get('/order/buy').status_code != 404
    with client:
        client.get('/order/buy')
        assert g.user['username'] == 'test'
        
    with app.app_context():
        client.post('/order/buy',
                    data={'symbol': 'AAPL', 'date': '2023-3-15', 'price': 63, 'share': 120, 'action': 'buy'})
        db = get_db()
        assert db.execute('SELECT * FROM portfolio').fetchone() is not None
        assert db.execute('SELECT balance from balance WHERE userid=1').fetchone()[0] == (1000000-63*120)
        # assert db.execute('SELECT shares FROM assets_info WHERE assetid = 1').fetchone()[0] == (4800000-120)
        # test if order is update
        order = db.execute("SELECT * FROM orders WHERE date='2023-3-15' and assetid=1 and userid=1").fetchone()
        assert order['action'] == 'buy'
        assert order['quantity'] == 120
def test_sell(client, auth, app):
    auth.login()
    with app.app_context():
        print("start testing sell")
        print("Buy 120 shares of AAPL")
        client.post('/order/buy',
                    data={'symbol': 'AAPL', 'date': '2023-3-15', 'price': 63, 'share': 120, 'action': 'buy'})
        # shares_owned = db.execute('SELECT shares FROM portfolio WHERE userid=1 and assetid=1').fetchone()[0]
        shares_owned = 120
        balance = get_balance(1)
        # post sell info
        print("Sell 100 shares of AAPL")
        client.post('/order/sell',
                    data={'symbol': 'AAPL', 'date': '2023-3-15', 'price': 63, 'share': 100, 'action': 'sell'})
        db = get_db()
        assert db.execute('SELECT shares FROM portfolio WHERE userid=1 and assetid=1').fetchone()[0] == (shares_owned-100)
        assert db.execute('SELECT balance from balance WHERE userid=1').fetchone()[0] == balance+(63*100)
        # assert db.execute('SELECT shares FROM assets_info WHERE assetid = 1').fetchone()[0] == (4800000-20)
        order = db.execute("SELECT * FROM orders WHERE date='2023-3-15' and assetid=1 and userid=1 and action='sell'").fetchone()
        assert order['quantity'] == 100
        
def test_get_balance(client, app):
    # ONLY after register can get intial balance
    response = client.post(
        '/auth/register', data={'username': 'user2', 'password': 'a'}
    )
    
    with app.app_context():
        id = get_db().execute('Select * from user').fetchone()['userid']
        assert get_balance(id) == 1000000
    
def test_get_assetid(app):
    with app.app_context():
        assert get_assetid('AAPL') == 1
        
def test_buy_asset(app, auth):
    # auth.login('jp584', '123456789')
    with app.app_context():
        buy_asset(1,1,1000000, 7560, 120, 0)
        db = get_db()
        assert db.execute('SELECT * FROM portfolio').fetchone() is not None
def test_data_processor():
    symbol = 'AAPL'
    assert get_company_name(symbol) == 'Apple'
    assert get_company_shares(symbol) is not None
