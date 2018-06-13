from flask import Flask, session, g
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from config import config
import datetime


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "basic"
login_manager.login_view = 'auth.checksign'
restapi = Api()


def create_app(config_name):
    app = Flask(__name__)
    manager = Manager(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)
    db.init_app(app)
    # db.create_all()
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .interactive import image as image_blueprint
    app.register_blueprint(image_blueprint, url_prefix='/api/image')

    # reflash session before request
    @app.before_request
    def before_request():
        if not current_user.is_anonymous:
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(days=365)
            session.modified = True
            g.user = current_user

    return manager, app
