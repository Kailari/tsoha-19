import re
import datetime
from application import app, db
from application.utils import try_redirect
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.comments.models import Comment
from application.auth.models import User
from application.wall.models import Subscription
from application.posts.forms import PostForm


@app.route("/wall/<id>/", methods=["GET", "POST"])
@login_required
def user_wall(id):
    user = User.query.get(id)
    subscriber_count = Subscription.query.filter_by(wall_id=user.wall.id).count()
    subscription_count = Subscription.query.filter_by(owner_id=user.id).count()
    post_count = Post.query.filter_by(owner_id=user.id).count()
    comment_count = Comment.query.filter_by(owner_id=user.id).count()

    if not user:
        return redirect(url_for("oops",
                                error="Invalid user ID"))

    if request.method == "GET":
        limit = 5
        older_than = request.args.get("older_than")
        if older_than == None:
            older_than = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)

        return render_template("wall/user_wall.html",
                               posts=Post.get_posts_for_user_wall(id,
                                                                  older_than=older_than,
                                                                  limit=limit),
                               user=user,
                               form=PostForm(),
                               limit=limit,
                               subscriber_count=subscriber_count,
                               subscription_count=subscription_count,
                               post_count=post_count,
                               comment_count=comment_count)

    form = PostForm(request.form)

    if not form.validate():
        return render_template("wall/user_wall.html",
                               posts=Post.get_posts_for_user_wall(id),
                               user=user,
                               form=form,
                               subscriber_count=subscriber_count,
                               subscription_count=subscription_count,
                               post_count=post_count,
                               comment_count=comment_count)

    content = re.sub(r"^\s+",
                     "",
                     form.content.data,
                     flags=re.MULTILINE).strip()
    owner_id = current_user.id
    wall_id = user.wall.id

    post = Post(content, owner_id, wall_id)
    db.session().add(post)
    db.session().commit()

    return redirect(url_for("user_wall",
                            id=id))


@app.route("/wall/<id>/unsubscribe", methods=["POST"])
@login_required
def wall_unsub(id):
    subscription = Subscription.query.filter_by(
        owner_id=current_user.id, wall_id=id).first()

    if subscription:
        db.session().delete(subscription)
        db.session().commit()

    return try_redirect("user_wall", **request.args, id=id)


@app.route("/wall/<id>/subscribe", methods=["POST"])
@login_required
def wall_sub(id):
    subscription = Subscription(owner_id=current_user.id, wall_id=id)
    db.session().add(subscription)
    db.session().commit()

    return try_redirect("user_wall", **request.args, id=id)
