from flask import Flask
from config import Config


def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # Initialization
    init_apps(app)
    register_blueprints(app)

    return app


def init_apps(app):
    pass


def register_blueprints(app):
    from app.main import main_blueprint

    app.register_blueprint(main_blueprint)
