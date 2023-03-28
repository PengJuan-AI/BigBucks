from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .auth import login_required
from .db import get_db

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

# ef
@bp.route('/ef', methods=('GET','POST'))
@login_required
def ef():
    return render_template('analysis/ef.html')

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
        hist = db.execute("SELECT strftime('%Y-%m-%d',history_date),close FROM assets_data WHERE symbol=?"
                      "ORDER BY history_date DESC",(symbol,)).fetchall()
        import pandas as pd
        df = pd.DataFrame(hist, columns=['date','price'])
        # print(df[0])
        print(df)
        data = {
            'date': list(df['date']),
            'price': list(df['price'])
        }
        return jsonify(data)
        # return hist