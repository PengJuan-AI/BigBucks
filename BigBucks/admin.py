from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for, session
)
from werkzeug.security import generate_password_hash
from .admin_auth import admin_login_required
from .db import get_db
from .Packages.get_weights import get_all_weights

bp = Blueprint("admin", __name__, url_prefix="/admin")

# admin home page
@bp.route('/')
@admin_login_required
def home():
    db = get_db()
    user_num = db.execute("SELECT COUNT(*) FROM user").fetchone()
    total_balance = db.execute("SELECT SUM(balance) FROM balance").fetchone()
    portfolio_data = db.execute("SELECT COUNT(DISTINCT symbol), SUM(shares) FROM portfolio").fetchone()
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
    return render_template('admin/home.html',user_num=user_num[0],total_balance=num_t_balance,portfolio_data=p_data)


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
    users = db.execute("SELECT userid, username FROM user")
    return render_template("admin/view_users.html",users=users)

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
    get_all_weights()
    pass