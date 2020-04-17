"""config.py
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Flask
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32).hex()

    # Flask-WTF
    WTF_CSRF_SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32).hex()

    # Flask-SQLAchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'temp/db.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    # Flask
    TESTING = True
    CSRF_ENABLED = False

    # Flask-WTF
    WTF_CSRF_ENABLED = False

    # Flask-SQLAchemy
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "DATABASE_URL") or f"sqlite:///{os.path.join(basedir, 'temp/test_db.db')}"
    )
