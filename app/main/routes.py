"""main/routes.py
"""

from . import main_blueprint
from .form import LoginForm, RecoverPasswordForm
from datetime import datetime
from app import db, mail
from app.models import User, Post
from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from flask_mail import Message


@main_blueprint.route("/")
def index():
    posts = Post.query.filter_by(can_display=True).order_by(
        Post.created_at.desc()).all()
    return render_template("index.html", title="My blog", posts=posts, current_post=None)


@main_blueprint.route("/view-post/<int:id>")
def view_post(id):
    posts = Post.query.filter_by(can_display=True).order_by(
        Post.created_at.desc()).all()
    post = Post.query.filter_by(id=id, can_display=True).first()
    post_time = post.parse_time()
    post_info = post.calculate_time_to_read()

    if post is not None:
        return render_template(
            "index.html", title="My blog", posts=posts, current_post=post, post_time=post_time, post_info=post_info
        )
    return render_template("unavailable.html", title="Unavailable")


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
            return redirect(url_for("admin.index"))

    return render_template("sign_in.html", title="Sign in", form=form)


@main_blueprint.route("/recover-password", methods=["GET", "POST"])
def recover_password():
    form = RecoverPasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            with current_app.app_context():
                msg = Message(
                    subject="Recover password",
                    sender=current_app.config.get("MAIL_USERNAME"),
                    recipients=[form.email.data],
                    body="This is a test body"
                )
                msg.send(mail)

            flash("An email has been sent to you. Check your inbox", "warning")
            return redirect(url_for("main.recover_password"))
    return render_template("recover_password.html", title="Recover Password", form=form)


@main_blueprint.route("/about-me")
def about_me():
    return render_template("about_me.html", title="About me / CV")


@main_blueprint.route("/logout")
def logout():
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

    logout_user()

    flash("Logout successful", "success")
    return redirect(url_for("main.sign_in"))
