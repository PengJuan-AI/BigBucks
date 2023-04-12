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

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE userid = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conf = request.form["conf"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        
        if password != conf :
            error = "Passwords do not match!"

        if error is None:
            try:
                initial_balance = 1000000
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.execute(
                    "INSERT INTO balance (balance) VALUES (?)",
                    (initial_balance,)
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered!"
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)
        session.clear()
        return render_template("auth/register.html",error=error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username!"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password!"

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user["userid"]
            session["user_name"] = user["username"]
            return redirect(url_for("index"))

        flash(error)
        session.clear()
        return render_template("auth/login.html",error=error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))

@bp.route("/account",methods=("GET","POST"))
@login_required
def account_settings():
    db = get_db()
    user_id = session["user_id"]
    ori_user = db.execute("SELECT username FROM user WHERE userid = ?",(user_id,)).fetchone()
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]
        error = None

        if not user_name:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "UPDATE user SET username = ?, password = ? WHERE userid = ?",
                    (user_name, generate_password_hash(password), user_id,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Username {user_name} is occupied!"
            else:
                info = "Successfully saved changes!"
                session["user_name"] = user_name
                return render_template("auth/account.html",info=info,user_name=user_name)

        flash(error)
        return render_template("auth/account.html",error=error,user_name=ori_user[0])

    else:
        return render_template("auth/account.html",user_name=ori_user[0])

