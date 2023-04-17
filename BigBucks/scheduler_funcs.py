from flask import Flask,render_template
from . import scheduler
from .db import get_db
from .order import update_new_data
from .Packages.live_data_processor import get_recent_data
import datetime

# Update all asset data with new date data
def job2():
    with scheduler.app.app_context():
        db = get_db()
        assets = db.execute("SELECT DISTINCT symbol FROM assets_data").fetchall()
        if not assets:
            print("None asset in database now")
        else:
            for a in assets:
                # print(a[0])
                update_new_data(a[0])
