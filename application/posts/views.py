from application import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.posts.forms import PostForm


@app.route("/posts", methods=["GET"])
@login_required
def posts_list():
    return render_template("posts/list.html", posts=Post.query.all())


@app.route("/posts/create/")
@login_required
def posts_form():
    return render_template("posts/create.html", form=PostForm())


@app.route("/posts/", methods=["POST"])
@login_required
def posts_create():
    form = PostForm(request.form)

    if not form.validate():
        return render_template("posts/create.html", form=form)

    post = Post(form.content.data)
    post.owner_id = current_user.id
    db.session().add(post)
    db.session().commit()

    return redirect(url_for("posts_list"))


@app.route("/posts/<post_id>/remove", methods=["POST"])
@login_required
def posts_remove(post_id):
    post = Post.query.get(post_id)
    if not post.owner_id == current_user.id:
        return render_template("posts/list.html",
                               error="Not authorized",
                               posts=Post.query.all())

    db.session().delete(post)
    db.session().commit()

    return redirect(url_for("posts_list"))


@app.route("/posts/<post_id>/edit", methods=["POST"])
@login_required
def posts_edit(post_id):
    post = Post.query.get(post_id)
    if not post.owner_id == current_user.id:
        return render_template("posts/list.html",
                               error="Not authorized",
                               posts=Post.query.all())

    content = request.form.get("content")
    post.content = content
    db.session().commit()

    return redirect(url_for("posts_list"))
