"""dashboard/routes.py
"""

from flask import flash, redirect, render_template, url_for
from . import dashboard_blueprint
from flask_login import login_required, logout_user


@dashboard_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")


@dashboard_blueprint.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Logged out user successful", "warning")
    return redirect(url_for("main.sign_in"))
