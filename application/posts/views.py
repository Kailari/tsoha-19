import re
from application import app, db
from application.utils import try_redirect
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.posts.forms import PostForm

from werkzeug.datastructures import MultiDict


@app.route("/posts/create/")
@login_required
def posts_form():
    return render_template("posts/create.html", form=PostForm())


@app.route("/posts/<post_id>/remove", methods=["POST"])
@login_required
def posts_remove(post_id):
    post = Post.query.get(post_id)
    if not post.owner_id == current_user.id:
        return redirect(url_for("oops", error="Not authorized"))

    db.session().delete(post)
    db.session().commit()

    return redirect(url_for("user_feed", **request.args))


@app.route("/posts/<post_id>/edit", methods=["GET", "POST"])
@login_required
def posts_edit(post_id):
    post = Post.query.get(post_id)
    if not post.owner_id == current_user.id:
        return redirect(url_for("oops", error="Not authorized"))

    if request.method == "GET":
        return render_template("posts/edit.html",
                               post_id=post_id,
                               form=PostForm(MultiDict({
                                   "content": post.content
                               })),
                               **request.args)

    form = PostForm(request.form)
    if not form.validate():
        return render_template("posts/edit.html",
                               post_id=post_id,
                               form=form,
                               **request.args)

    post.content = re.sub(r"^\s+",
                          "",
                          form.content.data,
                          flags=re.MULTILINE).strip()
    db.session().commit()

    return try_redirect("oops", **request.args)
