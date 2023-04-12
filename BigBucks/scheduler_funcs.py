from flask import Flask,render_template
from . import scheduler
from .db import get_db
import datetime

# # Set interval
# @scheduler.task('interval', id='job_1', seconds=30, misfire_grace_time=900)
# def job1():
#     print(str(datetime.datetime.now()) + ' Job 1 executed')

# @scheduler.task('interval', id='job_1', seconds=10, misfire_grace_time=900)
def job2():

    with scheduler.app.app_context():
        db = get_db()
        # time = str(datetime.datetime.now())
        print(str(datetime.datetime.now()) + ' Job 2 executed')
    # print(time+':', test[0])
    # return render_template('admin/home.html', time=time)