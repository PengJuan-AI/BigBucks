import os
from flask import Flask,render_template
import datetime
from flask_apscheduler import APScheduler

class Config(object):
    SCHEDULER_API_ENGABLED=True

scheduler = APScheduler()

# Set interval
@scheduler.task('interval', id='job_1', seconds=30, misfire_grace_time=900)
def job1():
    print(str(datetime.datetime.now()) + ' Job 1 executed')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        app.config.from_object(Config())

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('order/index.html')

    # Scheduler
    scheduler.init_app(app)
    scheduler.start()

    from . import db
    db.init_app(app)

    from BigBucks import auth   
    app.register_blueprint(auth.bp)
    
    from . import order
    app.register_blueprint(order.bp)

    from . import analysis
    app.register_blueprint(analysis.bp)

    from . import admin_auth
    app.register_blueprint(admin_auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    return app
