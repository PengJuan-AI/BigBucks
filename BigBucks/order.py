from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .db import get_db

bp = Blueprint('example', __name__, url_prefix='/order')

# buy



# sell
