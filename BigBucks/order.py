from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db
from .live_data_processor import get_company_name,get_company_shares, get_live_price

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
        print("In post")
        print(request.form)
        symbol = request.form['symbol']
        date = request.form['date']
        # price = float(request.form['price'])
        price = get_live_price(symbol)
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

    value = []
    for asset in portfolio:
        current_value = get_asset_value(asset['symbol'], id)
        value.append(current_value)

    if request.method=='POST':
        symbol = request.form['symbol']
        date = request.form['date']
        price = get_live_price(symbol)
        shares_traded = int(request.form['share'])
        action = request.form['action']
        error = None
        amount = price*shares_traded
        balance = get_balance(id)
        shares_owned = get_shares(id, symbol)

        if shares_traded>shares_owned:
            error = 'Shares owned are not enough'
        else:
            sell_asset(id,symbol,balance, amount, shares_traded, shares_owned)
            update_orders(date, id, symbol, shares_traded, price, action)

        flash(error)
        # return redirect(url_for('index'))

    return render_template('order/sell.html', info=info, portfolio=portfolio, value=value)


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

def get_outstanding(symbol):
    return get_company_shares(symbol)

def get_asset_name(symbol):
    return get_company_name(symbol)

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
        db.execute("UPDATE portfolio SET shares=? and value=? WHERE symbol=? and userid=?",
                   (shares_owned+shares_traded, value+amount, symbol, userid, )
                   )
    
    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?",(balance-amount, userid))
    
    db.commit()
        
def sell_asset(userid,symbol,balance, amount, shares_traded, shares_owned):
    print('In sell asset')
    db = get_db()

    if shares_traded==shares_owned:
        db.execute("DELETE FROM portfolio WHERE symbol=? and userid=?", (symbol, userid))
    else:
        value = get_asset_value(symbol, userid)
        db.execute("UPDATE portfolio SET shares=? and value=? WHERE symbol=? and userid=?",
               (shares_owned-shares_traded, value-amount, symbol, userid) )

    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?", (balance + amount, userid))

    db.commit()

# unnecessary in next step
# def update_asset_info(assetid, shares_traded):
#     '''
#     after one asset is traded, the outstanding shares of it decrease
#     '''
#     db = get_db()
#     outstanding = db.execute('SELECT shares FROM assets_info WHERE assetid=?', (assetid,)).fetchone()[0]
#     db.execute('UPDATE assets_info set shares=? WHERE assetid=?',
#                (outstanding-shares_traded, assetid)
#     )

def update_orders(date,id, symbol, shares, price, action ):
    db = get_db()
    db.execute('INSERT INTO orders (order_date, userid, symbol, quantity, price, action) VALUES (?,?,?,?,?,?)',
               (date, id, symbol,shares, price, action))
    db.commit()

# def update_asset_info(assetid, shares_traded):
#     '''
#     after one asset is traded, the outstanding shares of it decrease
#     '''
#     db = get_db()
#     outstanding = db.execute('SELECT shares FROM assets_info WHERE assetid=?', (assetid,)).fetchone()[0]
#     db.execute('UPDATE assets_info set shares=? WHERE assetid=?',
#                (outstanding-shares_traded, assetid)
#     )
#
#
# def update_orders(date,id, assetid, shares, price, action ):
#     db = get_db()
#     db.execute('INSERT INTO orders (order_date, userid, assetid, quantity, price, action) VALUES (?,?,?,?,?,?)',
#                (date, id, assetid,shares, price, action))

# query user's transaction records
@bp.route('/transaction',methods=('GET','POST'))
def transaction():
    id = g.user['userid']
    info = {}
    info['userid'] = id
    info['balance'] = get_balance(info['userid'])
    txn_record = get_db().execute('SELECT * FROM orders WHERE userid=?',(id,)).fetchall()
    print(txn_record)
    print(type(txn_record))
    return render_template('order/transaction.html', info=info, txn_record=txn_record)

# test
@bp.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    # 获取股票信息的逻辑代码
    symbol = request.form.get('stockname')
    stock_info = {'stockname': get_company_name(symbol), 'price': get_live_price(symbol), 'stocksymbol': symbol, 'outstanding': get_outstanding(symbol)}
    return jsonify(stock_info)