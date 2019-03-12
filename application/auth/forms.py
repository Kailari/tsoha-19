from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators, ValidationError

from application.auth.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", [
        validators.required(),
        validators.Length(
            min=4,
            max=32,
            message="username must be between 4 to 32 characters long")])

    password = PasswordField("Password", [validators.required()])

    class Meta:
        csrf = False


class UniqueUsername(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if User.user_with_username_exists(field.data):
            raise ValidationError(self.message)


class RegisterForm(FlaskForm):
    name = StringField("Name", [
        validators.required(),
        validators.Length(
            min=4,
            message="name must be at least 4 characters")])

    username = StringField("Username", [
        validators.required(),
        validators.Length(
            min=4,
            max=32,
            message="username must be between 4 to 32 characters long"),
        UniqueUsername(
            message="username is already taken")])

    password = PasswordField("Password", [
        validators.required(),
        validators.Length(
            min=6,
            message="password must be at least 6 characters long")])

    class Meta:
        csrf = False
