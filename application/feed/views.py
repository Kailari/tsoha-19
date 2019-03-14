from application import app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application.posts.models import Post


@app.route("/feed", methods=["GET"])
@login_required
def user_feed():
    return render_template("feed/user_feed.html",
                           posts=Post.get_posts_for_user_feed(current_user.id))
