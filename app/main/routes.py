from app.main import main_blueprint
from flask import render_template


@main_blueprint.route("/")
def index():
    return render_template("index.html", title="My blog")
