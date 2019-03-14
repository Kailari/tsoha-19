import os


def load_env():
    from dotenv import load_dotenv
    load_dotenv()


def configure_bcrypt(app):
    from flask_bcrypt import Bcrypt
    return Bcrypt(app)


def configure_database(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    if not os.environ.get("HEROKU"):
        app.config["SQLALCHEMY_ECHO"] = True

    from flask_sqlalchemy import SQLAlchemy
    return SQLAlchemy(app)


def load_models():
    from application.auth import models
    from application.posts import models
    from application.wall import models
    from application.comments import models


def load_views():
    from application import views
    from application.auth import views
    from application.posts import views
    from application.feed import views
    from application.wall import views
    from application.search import views


def configure_login_manager(app):
    from flask import redirect, url_for
    from flask_login import LoginManager
    from application.auth.models import User
    from os import urandom
    app.config["SECRET_KEY"] = urandom(32)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_message = "Please login to use this functionality."

    @login_manager.unauthorized_handler
    def redirect_to_login():
        return redirect(url_for("auth_login"))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)


def create_context_processors(app):
    @app.context_processor
    def timeago_processor():
        def timeago_format(time):
            import datetime
            import timeago
            return timeago.format(time, datetime.datetime.utcnow())
        return dict(timeago_format=timeago_format)
