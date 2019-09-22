from flask import Flask,render_template,redirect,request,url_for,session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    from app import models
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    from .frontend import frontend as frontend_blueprint
    app.register_blueprint(frontend_blueprint,url_prefix='/frontend')
    from .backend import backend as backend_blueprint
    app.register_blueprint(backend_blueprint,url_prefix='/api')
    from .analytics import analytics as analytics_blueprint
    app.register_blueprint(analytics_blueprint,url_prefix='/analytics')
    return app

# @app.route('/')
# def land():
#     redirect(url_for('auth.login'))
