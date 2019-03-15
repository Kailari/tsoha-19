import re
from application import app, db
from application.utils import try_redirect
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from application.posts.models import Post
from application.comments.models import Comment
from application.comments.forms import CommentForm

from werkzeug.datastructures import MultiDict


@app.route("/comments/<id>/conversation", methods=["GET", "POST"])
@login_required
def comments_conversation(id):
    post = Post.query.get(id)
    if not post:
        return redirect("oops", error="Post not found")

    if request.method == "GET":
        return render_template("comments/conversation.html",
                               post=post,
                               form=CommentForm(),
                               **request.args)

    form = CommentForm(request.form)
    if not form.validate():
        return render_template("comments/conversation.html",
                               post=post,
                               form=form,
                               **request.args)

    content = re.sub(r"^\s+",
                     "",
                     form.content.data,
                     flags=re.MULTILINE).strip()
    comment = Comment(content,
                      owner_id=current_user.id,
                      post_id=id)
    db.session().add(comment)
    db.session().commit()

    return redirect(url_for("comments_conversation",
                            id=id,
                            back=request.args.get("back"),
                            back_id=request.args.get("back_id")))


@app.route("/comments/<comment_id>/remove", methods=["POST"])
@login_required
def comments_remove(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment.owner_id == current_user.id:
        return redirect("oops", error="Not authorized")

    db.session().delete(comment)
    db.session().commit()

    return try_redirect("posts_list", **request.args)


@app.route("/comments/<comment_id>/edit", methods=["GET", "POST"])
@login_required
def comments_edit(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment.owner_id == current_user.id:
        return redirect("oops", error="Not authorized")

    if request.method == "GET":
        return render_template("comments/edit.html",
                               comment_id=comment_id,
                               form=CommentForm(MultiDict({
                                   "content": comment.content
                               })),
                               redir=request.args.get("redir"),
                               redir_id=request.args.get("redir_id"))

    form = CommentForm(request.form)
    if not form.validate():
        return render_template("comments/edit.html",
                               comment_id=comment_id,
                               form=form,
                               redir=request.args.get("redir"),
                               redir_id=request.args.get("redir_id"))

    comment.content = form.content.data
    db.session().commit()

    return try_redirect("comments_create", post_id=comment.post_id)
