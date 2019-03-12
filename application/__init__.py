from flask import Flask
app = Flask(__name__)

# Jinja extensions
import timeago, datetime

@app.context_processor
def timeago_processor():
    def timeago_format(time):
        print(type(time))
        return timeago.format(time, datetime.datetime.utcnow())
    return dict(timeago_format=timeago_format)

# Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Config
import os
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
    app.config["SQLALCHEMY_ECHO"] = True

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from application import views
from application.auth import models
from application.posts import models
from application.auth import views
from application.posts import views

# Login
from flask_login import LoginManager
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()
except:
    pass
