import os
from blinker import Namespace
from flask import Flask, session
from flask_wtf import CsrfProtect
from flask.ext.cors import CORS


csrf = CsrfProtect()

def create_app(config_file=None, config_object=None):
    """
    Bootstrap the flask application, registering blueprints, modules and other fun things.
    :param config_file: a python file containing key/values variables
    :param config_object: a python object (can be a dict) containing key/values variables
    :return: the app object
    """
    app = Flask(__name__, static_folder='public')

    # Configuration
    app.config.from_object('radar.settings.BaseConfig')
    app.environment = os.getenv('J4LP_RADAR_ENV', 'dev')

    if config_file:
        app.config.from_pyfile(config_file)
    if config_object:
        app.config.update(**config_object)

    #if app.environment != 'test':
        #csrf.init_app(app)

    cors = CORS(app, resources={r'/api/*': {'origins': '*',}}, allow_headers='Content-Type')

    # Database, Migration, Login and models
    from radar.models import db, login_manager, migrate
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Blueprints
    from radar.blueprints import AccountView, MetaView, RadarView
    AccountView.register(app)
    MetaView.register(app)
    RadarView.register(app)

    # OAuth
    from radar.oauth import oauth
    oauth.init_app(app)

    # API
    from radar.api import api_manager
    api_manager.init_app(app)

    from radar.utils import format_datetime, humanize
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['humanize'] = humanize

    @app.before_request
    def make_session():
        session.permanent = True

    return app
