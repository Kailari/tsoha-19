from application import app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user


@app.route("/feed", methods=["GET"])
@login_required
def user_feed():
    return render_template("feed/user_feed.html")