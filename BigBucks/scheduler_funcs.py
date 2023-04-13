from flask import Flask,render_template
from . import scheduler
from .db import get_db
from .order import update_new_data
from .Packages.live_data_processor import get_recent_data
import datetime


# # Set interval
# @scheduler.task('interval', id='job_1', seconds=30, misfire_grace_time=900)
# def job1():
#     print(str(datetime.datetime.now()) + ' Job 1 executed')

# @scheduler.task('interval', id='job_1', seconds=10, misfire_grace_time=900)
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
