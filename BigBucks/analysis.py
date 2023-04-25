from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
import pandas as pd
from .auth import login_required
from .db import get_db
from .Packages.efficient_frontier import cal_returns, cal_returns_with_date,get_ef, get_port_info
from .Packages.get_weights import get_portfolio_weights

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

# ef
@bp.route('/ef', methods=('GET','POST'))
@login_required
def ef():
    print("in ef")
    id = g.user['userid']
    port = get_portfolio_weights(id)
    error = None
    print('port in ef: \n',port)
    if not port:
        efficient_frontier = None
        port_info = {
            'port_return': 0,
            'port_vol': 0,
            'sharpe': 0
        }
        error = "Please add asset into your portfolio."
    else:
        weights, risk_return = get_ef(port)

        r, v, sharpe = get_port_info(port)
        efficient_frontier = {
            'weights': list(weights),
            'risk-return': list(risk_return)
        }
        port_info = {
            'port_return': round(r,2),
            'port_vol': round(v,2),
            'sharpe': round(sharpe,2)
        }
    print(port_info)
    return render_template('analysis/ef.html', ef=efficient_frontier, info=port_info, error=error)

# portfolio
# single asset
@bp.route('/single', methods=('GET','POST'))
@login_required
def single_asset():
    id = g.user['userid']
    portfolio = get_db().execute('SELECT * FROM portfolio WHERE userid=?', (id,)).fetchall()
    # index and asset return
    return render_template('analysis/single_asset.html',portfolio=portfolio)

# portfolio
# multiple asset
@bp.route('/multiple', methods=('GET','POST'))
@login_required
def multi_asset():
    id = g.user['userid']
    portfolio = get_db().execute('SELECT * FROM portfolio WHERE userid=?', (id,)).fetchall()
    # index and asset return
    date_returns = {}
    for asset in portfolio:
        symbol = asset[1]
        data = cal_returns_with_date(symbol)
        if len(date_returns)==0:
            date_returns['date'] = list(data['date'])
        date_returns[symbol] = list(data['returns'])

    return render_template('analysis/multi_asset.html',portfolio=portfolio, returns=date_returns)

@bp.route('/portfolio/<string:symbol>', methods=('GET','POST'))
def get_hist_data(symbol):
    db = get_db()

    if request.method == 'POST':
        hist_symbol = db.execute("SELECT strftime('%Y-%m-%d', history_date) as date, round(close, 2) as price FROM assets_data WHERE symbol=? ORDER BY history_date ASC", (symbol,)).fetchall()
        hist_SPY = db.execute("SELECT strftime('%Y-%m-%d', history_date) as SPY_date, round(close, 2) as SPY_price FROM assets_data WHERE symbol='SPY' ORDER BY history_date ASC").fetchall()

        df_symbol = pd.DataFrame(hist_symbol, columns=['date', 'price'])
        df_SPY = pd.DataFrame(hist_SPY, columns=['SPY_date', 'SPY_price'])

        df = pd.merge(df_symbol, df_SPY, left_on='date', right_on='SPY_date')
        df = df.drop(columns=['SPY_date'])

        data = {
            'date': list(df['date']),
            'price': list(df['price']),
            'price_SPY': list(df['SPY_price']),
            'return': list(cal_returns(symbol)[symbol]),
            'return_SPY': list(cal_returns('SPY')['SPY'])
        }

        return jsonify(data)