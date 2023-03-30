from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db
from efficient_frontier import get_ef, get_port_info

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

# ef
@bp.route('/ef', methods=('GET','POST'))
@login_required
def ef():
    id = g.user['userid']
    weights, returns, vols = get_ef(id)
    efficient_frontier = jsonify({
        'weights': weights,
        'returns': returns,
        'volatilities': vols
    })
    r, v, sharpe = get_port_info(id)
    port_info = jsonify({
        'port_return': r,
        'port_vol': v,
        'sharpe': sharpe
    })

    return render_template('analysis/ef.html', ef=efficient_frontier, info=port_info)

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