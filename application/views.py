from flask import render_template, request
from application import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/error")
def oops():
    return render_template("oops.html", **request.args)
