from flask import Flask,render_template
from flask_apscheduler import APScheduler
from .db import get_db
import datetime

scheduler = APScheduler()

def init_app(app):
    scheduler.init_app(app)
    scheduler.start()

# Set interval
@scheduler.task('interval', id='job_1', seconds=30, misfire_grace_time=900)
def job1():
    print(str(datetime.datetime.now()) + ' Job 1 executed')

@scheduler.task('interval', id='job_1', seconds=10, misfire_grace_time=900)
def job2():
    db = get_db()

    test = db.execute("SELECT DISTINCT symbol FROM assets_data").fetchone()
    time = str(datetime.datetime.now())

    print(time+':', test[0])
    # return render_template('admin/home.html', time=time)