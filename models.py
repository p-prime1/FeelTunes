import uuid
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username=None, email=None, password=None):
        self.id = uuid.uuid4()
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.username}>"
