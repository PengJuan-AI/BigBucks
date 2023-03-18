from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db

bp = Blueprint('order', __name__, url_prefix='/order')


# buy
@bp.route('/buy', methods=('GET','POST'))
@login_required
def buy():
    id = g.user['userid']
    if request.method == 'POST':
        print("POST request")
        symbol = request.form['symbol']
        date = request.form['date']
        price = request.form['price']
        shares = request.form['share']
        action = request.form['action']
        db = get_db()
        error = None
        balance = get_balance(id)
        amount = float(price)*float(shares)

        # check balance
        if balance< amount:
            error = "Balance is not enough"
        else:
            print("Buy Asset")
            assetid = get_assetid(symbol)
            buy_asset(id,assetid, balance, amount, shares)
            update_asset_info(assetid, shares)
            update_orders(date,id, assetid, shares, price, action )
        # check if asset exist
        return redirect(url_for('index'))
    elif request.method == 'GET': #GET
        info = {}
        info['userid'] = id
        info['balance'] = get_balance(info['userid'])
        
        return render_template('order/buy.html', info=info)

# sell

# Insert new order
def insert_new_order( time,price,shares, action):
    pass

# Get balance
def get_balance(id):
    balance = get_db().execute(
        'SELECT balance FROM Balance WHERE userid = ?',(id,)
    ).fetchone()[0]
    
    return balance

def get_assetid(symbol):
    id = get_db().execute(
        'SELECT assetid FROM Assets_info WHERE symbol = ?', (symbol,)
    ).fetchone()[0]

    return id

def buy_asset(userid,assetid,balance, amount, shares):
    '''
    buy asset: Portfoio change (shares increase), Balance change (balance decrease)
    '''
    db = get_db()
    sql = "SELECT * FROM portfolio WHERE assetid=? and userid=?"
    asset = db.execute(sql,(assetid,userid)).fetchone()
    
    # if the asset is not in portfolio, insert into portfolio, else update shares of the asset in portfolio
    if asset is None:
        db.execute("INSERT INTO portfolio (userid, assetid, shares) VALUES (?,?,?)",
                   (userid, assetid, shares)
                   )
    else:
        db.execute("UPDATE portfolio SET shares=? WHERE assetid=? and userid=?",
                   (asset['shares']+shares, assetid, userid)
                   )
    
    # Deduct amount from user's balance
    db.execute("UPDATE balance SET balance=? WHERE userid=?",(balance-amount, userid))
    
    db.commit()
        
def update_asset_info(assetid, shares):
    pass

def update_orders(date,id, assetid, shares, price, action ):
    pass