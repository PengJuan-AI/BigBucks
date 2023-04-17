from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db
from .Packages.live_data_processor import *
from datetime import datetime, timedelta
bp = Blueprint('order', __name__, url_prefix='/order')


# buy
@bp.route('/buy', methods=('GET','POST'))
@login_required
def buy():
    id = g.user['userid']
    info = {}
    info['userid'] = id
    info['balance'] = get_balance(info['userid'])

    if request.method == 'POST':
        print("In buy:")
        print(request.form)
        symbol = request.form['symbol']
        date = request.form['date']

        price = get_live_price_by_input(symbol,date)
        shares_traded = int(request.form['share'])
        action = request.form['action']
        error = None
        balance = get_balance(id)
        amount = price*shares_traded
        shares_owned = get_shares(id, symbol)

        # check balance
        if balance< amount:
            error = "Balance is not enough"
        else:
            buy_asset(id,symbol, balance, amount, shares_traded, shares_owned)
            update_orders(date,id, symbol, shares_traded, price, action )

        flash(error)

        # return info
        return render_template('order/buy.html', info=info)

    elif request.method == 'GET': #GET
        return render_template('order/buy.html', info=info)

# 'order/buy/apple'
# sell
@bp.route('/sell',methods=('GET','POST'))
def sell():
    id = g.user['userid']
    # get user basic infomation
    info = {}
    info['userid'] = id
    info['balance'] = get_balance(info['userid'])
    portfolio = get_db().execute('SELECT * FROM portfolio WHERE userid=?', (id,)).fetchall()

    date = datetime.today().strftime('%Y-%m-%d')
    price = []
    for asset in portfolio:
        current_price = get_live_price_by_input(asset['symbol'], date)
        price.append(current_price)

    if request.method=='POST':
        symbol = request.form['symbol']
        date = request.form['date']

        price = get_live_price_by_input(symbol, date)
        shares_traded = int(request.form['share'])
        action = request.form['action']
        error = None
        amount = price*shares_traded
        balance = get_balance(id)
        shares_owned = get_shares(id, symbol)

        if shares_traded>shares_owned:
            error = 'Shares owned are not enough'
            print(error)
        else:
            sell_asset(id,symbol,balance, amount, shares_traded, shares_owned)
            update_orders(date, id, symbol, shares_traded, price, action)

        flash(error)
        # return redirect(url_for('index'))

    return render_template('order/sell.html', info=info, portfolio=portfolio, price=price)


# Get balance
def get_balance(id):
    balance = get_db().execute(
        'SELECT balance FROM Balance WHERE userid = ?',(id,)
    ).fetchone()[0]
    return balance

# use functions from data_processor
def get_shares(userid, symbol):
    shares = get_db().execute(
        'SELECT shares FROM portfolio WHERE userid = ? and symbol=?', (userid, symbol)
    ).fetchone()
    if shares is None:
        return 0
    else:
        return shares[0]

def get_outstanding(input):
    return get_company_shares_by_input(input)

def get_asset_name(input):
    return get_name_by_input(input)

def get_asset_value(symbol,userid):
    return get_db().execute(
        "SELECT value FROM portfolio WHERE userid = ? and symbol=?", (userid, symbol)
    ).fetchone()[0]

def buy_asset(userid,symbol,balance, amount, shares_traded, shares_owned):
    '''
    buy asset: Portfoio change (shares increase), Balance change (balance decrease)
    '''
    db = get_db()
    # if the asset is not in portfolio, insert into portfolio, else update shares of the asset in portfolio
    if shares_owned == 0:
        db.execute("INSERT INTO portfolio (userid, symbol, shares, value) VALUES (?,?,?,?)",
                   (userid, symbol, shares_traded, amount)
                   )
    else:
        value = get_asset_value(symbol, userid)
        db.execute("UPDATE portfolio SET shares=?, value=? WHERE symbol=? and userid=?",
                   (shares_owned+shares_traded, value+amount, symbol, userid, )
                   )
    
    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?",(balance-amount, userid))
    
    db.commit()

    # add historical data of this asset
    update_hist_data(symbol)
        
def sell_asset(userid,symbol,balance, amount, shares_traded, shares_owned):
    print('In sell asset')

    db = get_db()

    if shares_traded==shares_owned:
        db.execute("DELETE FROM portfolio WHERE symbol=? and userid=?", (symbol, userid))
    else:
        value = get_asset_value(symbol, userid)
        db.execute("UPDATE portfolio SET shares=?, value=? WHERE symbol=? and userid=?",
               (shares_owned-shares_traded, value-amount, symbol, userid) )
        shares = db.execute("SELECT shares from portfolio WHERE symbol=? and userid=?",(symbol, userid)).fetchone()[0]
        print(shares)
    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?", (balance + amount, userid))

    db.commit()

def update_orders(date,id, symbol, shares, price, action ):
    db = get_db()
    db.execute('INSERT INTO orders (order_date, userid, symbol, quantity, price, action) VALUES (?,?,?,?,?,?)',
               (date, id, symbol,shares, price, action))
    db.commit()

def update_hist_data(symbol):
    data = get_data_by_input(symbol)
    update_asset_data(symbol, data)

def update_new_data(symbol):
    # print("In update new data")
    data = get_recent_data(symbol)
    update_asset_data(symbol, data)

def update_asset_data(symbol,data):
    db = get_db()
    sql = "INSERT OR REPLACE INTO Assets_data (symbol, history_date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    for index, row in data.iterrows():
        symbol = symbol
        history_date = index.strftime('%Y-%m-%d')
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        adj_close_price = row['Adj Close']
        volume = row['Volume']
        db.execute(sql, (symbol, history_date, open_price, high_price, low_price, close_price, adj_close_price, volume))

    db.commit()


# query user's transaction records
@bp.route('/transaction',methods=('GET','POST'))
def transaction():
    id = g.user['userid']
    info = {}
    info['userid'] = id
    info['balance'] = get_balance(info['userid'])
    txn_record = get_db().execute('SELECT * FROM orders WHERE userid=?',(id,)).fetchall()
    # print(txn_record)
    # print(type(txn_record))
    return render_template('order/transaction.html', info=info, txn_record=txn_record)

# test
@bp.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    # 获取股票信息的逻辑代码
    symbol = request.form.get('stockname')
    symbol = request.form.get('date')
    stock_info = {'stockname': get_name_by_input(symbol), 'price': get_live_price_by_input(symbol,date), 'stocksymbol': get_symbol_by_input(symbol), 'outstanding': get_outstanding(symbol)}
    return jsonify(stock_info)