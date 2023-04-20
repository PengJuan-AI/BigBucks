from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for, session
)
from werkzeug.security import generate_password_hash
from .admin_auth import admin_login_required
from .db import get_db
from .Packages.get_weights import get_all_weights
from .Packages.efficient_frontier import get_ef,get_port_info
from .Packages.live_data_processor import get_company_name
import datetime

bp = Blueprint("admin", __name__, url_prefix="/admin")

# admin home page
@bp.route('/')
@admin_login_required
def home():
    db = get_db()
    user_num = db.execute("SELECT COUNT(*) FROM user").fetchone()
    total_balance = db.execute("SELECT SUM(balance) FROM balance").fetchone()
    portfolio_data = db.execute("SELECT COUNT(DISTINCT symbol), SUM(shares) FROM portfolio").fetchone()
    asset_data = db.execute("SELECT symbol, MAX(history_date) date FROM assets_data GROUP BY symbol").fetchall()
    # do not show none
    if not total_balance[0]:
        num_t_balance = 0
    else:
        num_t_balance = total_balance[0]
    p_data = {}
    if not portfolio_data[1]:
        p_data['shares'] = 0
    else:
        p_data['shares'] = portfolio_data[1]
    p_data['asset'] = portfolio_data[0]
    assets = []
    for a in asset_data:
        data = {}
        data['symbol'] = a[0]
        data['date'] = a[1]
        assets.append(data)

    return render_template('admin/home.html',assets=assets, user_num=user_num[0],total_balance=num_t_balance,portfolio_data=p_data)


# add new admin
@bp.route('/add_admin', methods=('GET','POST'))
@admin_login_required
def add_admin():
    if request.method == "POST":
        admin_name = request.form["admin_name"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not admin_name:
            error = "Admin name is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO admin (admin_name, password) VALUES (?, ?)",
                    (admin_name, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"Admin {admin_name} is already registered!"
            else:
                info = "Successfully added a new admin!"
                return render_template("admin/add.html",info=info)

        flash(error)
        return render_template("admin/add.html",error=error)

    return render_template("admin/add.html")

# view user data
@bp.route('/view_users')
@admin_login_required
def view_users():
    db = get_db()
    users = db.execute("SELECT u.userid, u.username, u.email, u.date, b.balance \
    FROM user AS u \
    INNER JOIN balance AS b \
    ON b.userid = u.userid \
    ORDER BY u.userid")
    return render_template("admin/view_users.html",users=users)

# view user stock data
@bp.route('/view_stocks')
@admin_login_required
def view_stocks():
    db = get_db()
    # stocks = db.execute("SELECT symbol, SUM(shares) as ttl_shares FROM portfolio GROUP BY symbol ORDER BY ttl_shares")
    stocks=[]
    stock_info = db.execute("SELECT symbol, SUM(shares), SUM(value) FROM portfolio GROUP BY symbol ORDER BY symbol").fetchall()
    for s in stock_info:
        stock = {}
        stock['symbol'] = s[0]
        stock['name'] = get_company_name(s[0])
        stock['shares_held'] = s[1]
        stock['price_per_share'] = round(s[2]/s[1],2)
        print(stock)
        stocks.append(stock)

    return render_template("admin/view_stocks.html",stocks=stocks)

# view admin data
@bp.route('/view_admins')
@admin_login_required
def view_admins():
    db = get_db()
    admins = db.execute("SELECT adminid, admin_name FROM admin")
    return render_template("admin/view_admins.html",admins=admins)

@bp.route('/risk_return')
@admin_login_required
def risk_return():
    portfolio = get_all_weights()
    error = None
    if not portfolio:
        risk_re = 0
        port_info = {
            'rtn': 0,
            'vol': 0,
            'sharpe': 0
        }
        error = "Not users buy any assets yet."
    else:
        weights, risk_re =  get_ef(portfolio)
        r, v, sharpe = get_port_info(portfolio)
        port_info = {
            'rtn': round(r,2),
            'vol': round(v,2),
            'sharpe': round(sharpe,2)
        }
    
    return render_template("admin/risk_return.html",ef=risk_re,info=port_info,error=error)

@bp.route('/today_orders')
@admin_login_required
def today_orders():
    db = get_db()
    today = datetime.date.today()
    info = []
    error = None
    result = db.execute("SELECT * FROM orders WHERE order_date=?",(today,)).fetchall()

    if not result:
        error = "No users buy any asset today."
    else:
        # num = 0
        for order in result:
            _info = {}
            _info['Date'] = order[1]
            _info['symbol'] = order[3]
            _info['name'] = get_company_name(order[3])
            _info['shares'] = order[4]
            _info['price'] = order[5]
            _info['action'] = order[6]
            info.append(_info)

        print(_info)

    return render_template("admin/today_orders.html",info=info,error=error)

# @bp.route('/scheduler', methods=('GET','POST'))
# @admin_login_required
# def scheduler_test():
#     from scheduler import job2
#     time = job2()
#
#     return render_template("admin/scheduler.html", time=time)


@bp.route('/account_settings', methods=('GET','POST'))
@admin_login_required
def account_settings():
    db = get_db()
    admin_id = session["admin_id"]
    ori_admin = db.execute("SELECT admin_name FROM admin WHERE adminid = ?",(admin_id,)).fetchone()
    if request.method == "POST":
        admin_name = request.form["admin_name"]
        password = request.form["password"]
        error = None

        if not admin_name:
            error = "Admin name is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "UPDATE admin SET admin_name = ?, password = ? WHERE adminid = ?",
                    (admin_name, generate_password_hash(password), admin_id,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Admin name {admin_name} is occupied!"
            else:
                info = "Successfully saved changes!"
                session["admin_name"] = admin_name
                return render_template("admin/edit_acnt.html",info=info,admin_name=admin_name)

        flash(error)
        return render_template("admin/edit_acnt.html",error=error,admin_name=ori_admin[0])

    else:
        return render_template("admin/edit_acnt.html",admin_name=ori_admin[0])
