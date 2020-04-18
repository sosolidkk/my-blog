"""app/__init__.py
"""

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
admin = Admin()

login = LoginManager()
login.login_view = "main.sign_in"
login.login_message_category = "warning"


def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    # Initialization
    init_apps(app)
    register_blueprints(app)
    add_admin_views(admin, db)

    return app


def init_apps(app):
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def add_admin_views(admin, db):
    from flask_admin.contrib.sqla import ModelView
    from app.models import Post

    admin.add_view(ModelView(Post, db.session))


def register_blueprints(app):
    from app.main import main_blueprint
    from app.dashboard import dashboard_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(dashboard_blueprint)
