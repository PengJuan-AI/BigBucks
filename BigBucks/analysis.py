from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db
from Packages.efficient_frontier import get_ef, get_port_info
from Packages.get_weights import get_portfolio_weights

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

# ef
@bp.route('/ef', methods=('GET','POST'))
@login_required
def ef():
    id = g.user['userid']
    port = get_portfolio_weights(id)
    error = None
    if not port:
        efficient_frontier = None
        port_info = {
            'port_return': 0,
            'port_vol': 0,
            'sharpe': 0
        }
        error = "Please add asset into your portfolio."
    else:
        print("Initial")
        print(port)
        weights, returns, vols = get_ef(port)
        print("Second")
        print(port)
        r, v, sharpe = get_port_info(port)
        efficient_frontier = {
            'weights': list(weights),
            'returns': list(returns),
            'volatilities': list(vols)
        }
        port_info = {
            'port_return': round(r,2),
            'port_vol': round(v,2),
            'sharpe': round(sharpe,2)
        }

    return render_template('analysis/ef.html', ef=efficient_frontier, info=port_info, error=error)

# market
@bp.route('/market', methods=('GET','POST'))
@login_required
def market():
    return render_template('analysis/market.html')

# portfolio
@bp.route('/portfolio', methods=('GET','POST'))
@login_required
def portfolio():
    id = g.user['userid']
    portfolio = get_db().execute('SELECT * FROM portfolio WHERE userid=?', (id,)).fetchall()
    return render_template('portfolio.html',portfolio=portfolio)

@bp.route('/portfolio/<string:symbol>', methods=('GET','POST'))
def get_hist_data(symbol):
    db = get_db()

    if request.method=='POST':
        hist = db.execute("SELECT strftime('%Y-%m-%d',history_date),round(close,2) FROM assets_data WHERE symbol=?"
                      "ORDER BY history_date ASC",(symbol,)).fetchall()
        import pandas as pd
        df = pd.DataFrame(hist, columns=['date','price'])
        data = {
            'date': list(df['date']),
            'price': list(df['price'])
        }
        return jsonify(data)
        # return hist