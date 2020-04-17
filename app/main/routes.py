"""main/routes.py
"""

from flask import flash, redirect, render_template, request, url_for
from . import main_blueprint
from .form import LoginForm
from app.models import User, Post
from flask_login import login_user


@main_blueprint.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", title="My blog", posts=posts, current_post=None)


@main_blueprint.route("/view-post/<int:id>")
def view_post(id):
    posts = Post.query.all()
    post = [post for post in posts if post.id == id][0]

    return render_template("index.html", title="My blog", posts=posts, current_post=post)


@main_blueprint.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password", "danger")
                return redirect(url_for("main.sign_in"))

            login_user(user, remember=form.remember_me.data)
            flash("Logged in successful", "success")
            return redirect(url_for("dashboard.dashboard"))

    return render_template("sign_in.html", title="Sign in", form=form)
