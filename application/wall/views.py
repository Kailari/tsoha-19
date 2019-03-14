from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.auth.models import User
from application.posts.forms import PostForm


@app.route("/wall/<user_id>/", methods=["GET", "POST"])
@login_required
def user_wall(user_id):
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for("user_feed",
                                error="Invalid user ID"))

    if request.method == "GET":
        return render_template("wall/user_wall.html",
                               posts=Post.get_posts_for_user_wall(user_id),
                               user=user,
                               form=PostForm())

    form = PostForm(request.form)

    if not form.validate():
        return render_template("wall/user_wall.html",
                               posts=Post.get_posts_for_user_wall(user_id),
                               user=user,
                               form=form)

    content = form.content.data
    owner_id = current_user.id
    wall_id = user.wall.id
    
    post = Post(content, owner_id, wall_id)
    post.owner_id = current_user.id
    db.session().add(post)
    db.session().commit()

    return redirect(url_for("user_wall",
                            user_id=user_id))
