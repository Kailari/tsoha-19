from application import app
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from werkzeug.datastructures import MultiDict

from application.search.forms import SearchForm
from application.auth.models import User


@app.route("/search/", methods=["GET"])
@login_required
def user_search():
    name_filter = request.args.get("name_filter") or ""

    form = SearchForm(MultiDict({
        "name_filter": name_filter
    }))

    if name_filter == "":
        users = []
    else:
        users = User.find_users_by_partial_username(user_id=current_user.id,
                                                    name_filter=name_filter)

    return render_template("search/find_users.html",
                           form=form,
                           users=users,
                           name_filter=name_filter)
