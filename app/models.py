"""app/models.py
"""

from app import db
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    Class that represents a user of the application
    The following attributes of a user are stored in this table:
        username
        email address
        password (hashed using wekzeug.security)
        description of user (filled later on the dashboard)
        date that the user was created
        last time user has logged in
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True)
    posts = db.relationship("Post", backref="author", lazy="dynamic")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.set_password(password)
        self.about_me = ""

    def __repr__(self):
        return f"Author <{self.username}>"

    def set_password(self, password):
        return generate_password_hash(password, salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def parse_time(self):
        date = self.last_seen.strftime("%d/%m/%Y")
        hour = self.last_seen.strftime("%H:%M:%S")

        return date, hour


class Post(db.Model):
    """
    Class that represents a post of the use in the application
    The following attributes of a user are stored in this table:
        id of the post
        title of the post
        body of the post
        timestamp of the creation
    """

    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.UnicodeText)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    can_display = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def parse_time(self):
        date = self.created_at.strftime("%d/%m/%Y")
        hour = self.created_at.strftime("%H:%M")

        return date, hour

    def __repr__(self):
        return f"<Post: {self.title}>"

    def __unicode__(self):
        return self.title
