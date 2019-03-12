from application import app, db
from flask import render_template, request, redirect, url_for
from application.posts.models import Post
from application.posts.forms import PostForm

@app.route("/posts", methods=["GET"])
def posts_list():
    return render_template("posts/list.html", posts = Post.query.all())


@app.route("/posts/create/")
def posts_form():
    return render_template("posts/create.html", form = PostForm())


@app.route("/api/posts/", methods=["POST"])
def posts_create():
    post = Post(request.form.get("content"))

    db.session().add(post)
    db.session().commit()

    return redirect(url_for("posts_list"))


@app.route("/api/posts/<post_id>/", methods=["POST"])
def posts_edit(post_id):
    content = request.form.get("content")
    post = Post.query.get(post_id)
    post.content = content
    db.session().commit()

    return redirect(url_for("posts_list"))
