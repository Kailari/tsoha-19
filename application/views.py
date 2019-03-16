from flask import render_template, request, url_for, redirect
from flask_login import current_user
from application import app


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user_feed', id=current_user.id))
    else:
        return render_template("index.html")


@app.route("/error")
def oops():
    return render_template("oops.html", **request.args)
