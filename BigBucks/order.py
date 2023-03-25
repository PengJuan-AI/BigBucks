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
        # assetid = get_assetid(symbol)
        shares_owned = get_shares(id, symbol)

        # check balance
        if balance< amount:
            error = "Balance is not enough"
        else:
            buy_asset(id,symbol, balance, amount, shares_traded, shares_owned)
            # update_asset_info(assetid, shares_traded)
            update_orders(date,id, symbol, shares_traded, price, action )

        flash(error)

        return info
    
    elif request.method == 'GET': #GET
        return render_template('order/buy.html', info=info)

# 'order/buy/apple'
# sell
@bp.route('/sell',methods=('GET','POST'))
def sell():
    id = g.user['userid']
    if request.method=='POST':
        symbol = request.form['symbol']
        date = request.form['date']
        price = get_live_price(symbol)
        shares_traded = int(request.form['share'])
        action = request.form['action']
        error = None
        amount = price*shares_traded
        balance = get_balance(id)
        # assetid = get_assetid(symbol)
        shares_owned = get_shares(id, symbol)

        if shares_traded>shares_owned:
            error = 'Shares owned are not enough'
        else:
            sell_asset(id,symbol,balance, amount, shares_traded, shares_owned)
            # update_asset_info(assetid, -shares_traded)
            update_orders(date, id, symbol, shares_traded, price, action)

        flash(error)
        return redirect(url_for('index'))

    elif request.method == 'GET': #GET
        info = {}
        info['userid'] = id
        info['balance'] = get_balance(info['userid'])
        portfolio = get_db().execute('SELECT * FROM portfolio WHERE userid=?',(id,)).fetchall()

        price = []
        for asset in portfolio:
            current_price = get_live_price(asset['symbol'])
            price.append(current_price)

    return render_template('order/sell.html', info=info, portfolio=portfolio, price = price)


# Get balance
def get_balance(id):
    balance = get_db().execute(
        'SELECT balance FROM Balance WHERE userid = ?',(id,)
    ).fetchone()[0]
    
    return balance

# def get_assetid(symbol):
#     id = get_db().execute(
#         'SELECT assetid FROM Assets_info WHERE symbol = ?', (symbol,)
#     ).fetchone()[0]
# 
#     return id

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

def buy_asset(userid,symbol,balance, amount, shares_traded, shares_owned):
    '''
    buy asset: Portfoio change (shares increase), Balance change (balance decrease)
    '''
    db = get_db()
    # if the asset is not in portfolio, insert into portfolio, else update shares of the asset in portfolio
    if shares_owned == 0:
        db.execute("INSERT INTO portfolio (userid, symbol, shares) VALUES (?,?,?)",
                   (userid, symbol, shares_traded)
                   )
    else:
        db.execute("UPDATE portfolio SET shares=? WHERE symbol=? and userid=?",
                   (shares_owned+shares_traded, symbol, userid)
                   )
    
    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?",(balance-amount, userid))
    
    db.commit()
        
def sell_asset(userid,symbol,balance, amount, shares_traded, shares_owned):
    print('In sell asset')
    db = get_db()
    
    db.execute("UPDATE portfolio SET shares=? WHERE symbol=? and userid=?",
               (shares_owned-shares_traded, symbol, userid) )

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