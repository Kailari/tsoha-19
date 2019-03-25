import datetime
from application import app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.posts.models import Post


@app.route("/feed", methods=["GET"])
@login_required
def user_feed():
    limit = 5
    older_than = request.args.get("older_than")
    if older_than == None:
        older_than = datetime.datetime.utcnow()

    return render_template("feed/user_feed.html",
                           posts=Post.get_posts_for_user_feed(current_user.id,
                                                              older_than=older_than,
                                                              limit=limit),
                           limit=limit)
