import os
from flask import Flask,render_template
import datetime

# initialize scheduler
from flask_apscheduler import APScheduler
scheduler = APScheduler()

class SchedulerConfig(object):
    JOBS=[
        {
            'id':'update_asset_data',
            'func': 'BigBucks.scheduler_funcs:job2',
            'args': None,
            'trigger':{
                'type': 'interval',
                'seconds':10
            }
        }
    ]
    SCHEDULER_API_ENGABLED=True


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

    app.config.from_object(SchedulerConfig)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return render_template('order/index.html')

    # Scheduler
    # from . import scheduler
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
