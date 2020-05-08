"""app/__init__.py
"""

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.admin_views import AdminModelView

db = SQLAlchemy()
login = LoginManager()
mail = Mail()
migrate = Migrate()
admin = Admin(name="My blog", index_view=AdminModelView())


def create_app(config_class=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    init_apps(app)
    register_blueprints(app)
    add_admin_views(admin, db)
    add_error_views(app)

    return app


def init_apps(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    login.init_app(app)
    login.login_view = "main.sign_in"
    login.login_message_category = "warning"

    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def add_admin_views(admin, db):
    from app.admin_views import PostModelView
    from app.models import Post

    admin.add_view(PostModelView(Post, db.session))


def add_error_views(app):
    from app.error_views import page_not_found, internal_server_error

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)


def register_blueprints(app):
    from app.main import main_blueprint

    app.register_blueprint(main_blueprint)
