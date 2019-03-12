from application import app, db
from flask import render_template, request, redirect, url_for
from application.posts.models import Post

@app.route("/posts", methods=["GET"])
def posts_list():
    return render_template("posts/list.html", posts = Post.query.all())


@app.route("/posts/create/")
def posts_form():
    return render_template("posts/create.html")


@app.route("/api/posts/", methods=["POST"])
def posts_create():
    post = Post(request.form.get("content"))

    db.session().add(post)
    db.session().commit()

    return redirect(url_for("posts_list"))
