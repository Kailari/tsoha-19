from flask import render_template, request, redirect, url_for
from flask_login import login_user

from application import app, bcrypt, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm


@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/login.html",
                               form=LoginForm())

    form = LoginForm(request.form)

    if not form.validate():
        return render_template("auth/login.html",
                               form=form)

    user = User.find_user_by_username(form.username.data)
    if not bcrypt.check_password_hash(user.password_hash, form.password.data):
        return render_template("auth/login.html",
                               form=form,
                               error="Invalid username or password")

    login_user(user)
    print("User " + user.name + " logged in")
    return redirect(url_for("index"))


@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/register.html",
                               form=RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth/register.html",
                               form=form)

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

    print("hash: " + pw_hash)

    user = User(name=form.name.data,
                username=form.username.data,
                password_hash=pw_hash)
    db.session().add(user)
    db.session().commit()

    print("User " + user.name + " registered")
    return redirect(url_for("index"))
