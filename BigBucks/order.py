from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db

bp = Blueprint('example', __name__, url_prefix='/order')


# buy
@bp.route('/buy', methods=('GET','POST'))
@login_required
def buy():
    id = g.user['userid']
    if request.method == 'POST':
        symbol = request.form['symbol']
        time = request.form['time']
        price = request.form['price']
        shares = request.form['share']
        action = request.form['action']
        db = get_db()
        error = None
        balance = get_balance(id)
        amount = price*shares
        # check balance
        if balance< amount:
            error = "Balance is not enough"
        else:
            assetid = get_assetid(symbol)
            buy_asset(id,amount)
        # check if asset exist
        
    elif request.method == 'GET': #GET
        info = {}
        info['userid'] = id
        info['balance'] = get_balance(info['userid'])
        db = get_db()
        db.execute()
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