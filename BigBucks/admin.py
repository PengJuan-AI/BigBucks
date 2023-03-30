from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, url_for
)
from .admin_auth import admin_login_required
from .db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin")

# admin home page
@bp.route('/', methods=('GET','POST'))
@admin_login_required
def home():
    return render_template('admin/home.html')