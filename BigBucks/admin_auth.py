import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .db import get_db

bp = Blueprint("admin_auth", __name__, url_prefix="/adminauth")


def admin_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            return redirect(url_for("admin_auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_admin():
    admin_id = session.get("admin_id")

    if admin_id is None:
        g.admin = None
    else:
        g.admin = (
            get_db().execute("SELECT * FROM admin WHERE adminid = ?", (admin_id,)).fetchone()
        )

@bp.route("/adminlogin", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        admin_name = request.form["admin_name"]
        password = request.form["password"]
        db = get_db()
        error = None
        admin = db.execute(
            "SELECT * FROM admin WHERE admin_name = ?", (admin_name,)
        ).fetchone()

        if admin is None:
            error = "Admin not exist!"
        elif not check_password_hash(admin["password"], password):
            error = "Incorrect password!"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["admin_id"] = admin["adminid"]
            session["admin_name"] = admin["admin_name"]
            return redirect(url_for("admin.home"))

        flash(error)
        session.clear()
        return render_template("admin/login.html",error=error)

    return render_template("admin/login.html")


@bp.route("/adminlogout")
def logout():
    session.clear()
    return redirect(url_for("admin.home"))
