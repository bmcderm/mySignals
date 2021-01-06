# NOTE: DO NOT FORMAT THIS FILE!!!

import os

from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()
MIGRATE = Migrate()
BOOTSTRAP = Bootstrap()

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' if Config.DEBUG else '0'


def createApp():
    app = Flask(__name__)
    app.debug = Config.DEBUG
    app.config.from_object(Config)

    # Initialize extensions
    DB.init_app(app)
    BOOTSTRAP.init_app(app)
    MIGRATE.init_app(app, DB)

    # Initalize blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    return app


from app import models
