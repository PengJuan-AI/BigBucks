import pytest
from flask import g, session
from BigBucks.db import get_db
from BigBucks.order import get_balance, buy_asset, get_company_name,get_company_shares,update_asset_data
from Packages.live_data_processor import get_live_price_by_input

def test_buy(client, auth,app):
    auth.login()
    symbol = 'AAPL'
    date = '2023-4-21'
    price = get_live_price_by_input(symbol, date)

    assert client.get('/order/buy').status_code != 404
        
    with app.app_context():
        client.post('/order/buy',
                    data={'symbol': symbol, 'date': date, 'price': price, 'share': 100, 'action': 'buy'})
        db = get_db()
        portfolio = db.execute('SELECT * FROM portfolio WHERE userid=1').fetchall()
        assert portfolio[0]['shares'] == 100
        assert portfolio[0]['value'] == price*100
        assert db.execute('SELECT balance from balance WHERE userid=1').fetchone()[0] == (1000000-price*100)
        # test if order is update
        order = db.execute("SELECT * FROM orders WHERE order_date=? and symbol=? and userid=1",(date, symbol)).fetchone()
        assert order['action'] == 'buy'
        assert order['quantity'] == 100
        # test if asset data is inserted
        asset = db.execute("SELECT * FROM assets_data WHERE symbol=? ORDER BY history_date DESC",(symbol,)).fetchone()
        assert asset is not None
        # assert asset[1].strftime('%Y-%m-%d') == '2023-03-24'

def test_sell(client, auth, app):
    auth.login()
    symbol = 'AAPL'
    buy_date = '2023-4-21'
    sell_date = '2023-4-24'
    buy_price = get_live_price_by_input(symbol, buy_date)
    sell_price = get_live_price_by_input(symbol, sell_date)

    with app.app_context():
        shares_owned = 200
        db = get_db()

        client.post('/order/buy',
                    data={'symbol': symbol, 'date': buy_date, 'price': buy_price, 'share': shares_owned, 'action': 'buy'})
        assert db.execute('SELECT shares FROM portfolio WHERE userid=1 and symbol=?',(symbol,)).fetchone()[0] == 200

        balance = get_balance(1)
        # post sell info
        print("Sell 100 shares of AAPL")
        client.post('/order/sell',
                    data={'symbol': symbol, 'date':sell_date, 'price': sell_price, 'share': 100, 'action': 'sell'})

        portfolio = db.execute('SELECT * FROM portfolio WHERE userid=1').fetchall()
        assert portfolio[0]['shares'] == 100
        assert portfolio[0]['value'] == buy_price*200 - sell_price*100
        assert db.execute('SELECT balance from balance WHERE userid=1').fetchone()[0] == balance+(sell_price*100)
        order = db.execute("SELECT * FROM orders WHERE order_date=? and symbol=? and userid=1", (sell_date, symbol)).fetchone()
        assert order['action'] == 'sell'

def test_data_processor():
    symbol = 'AAPL'
    assert get_company_name(symbol) == 'Apple Inc.'
    assert get_company_shares(symbol) is not None
