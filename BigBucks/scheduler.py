from flask import Flask,render_template
from flask_apscheduler import APScheduler
import datetime

scheduler = APScheduler()

def init_app(app):
    scheduler.init_app(app)
    scheduler.start()

# Set interval
@scheduler.task('interval', id='job_1', seconds=30, misfire_grace_time=900)
def job1():
    print(str(datetime.datetime.now()) + ' Job 1 executed')