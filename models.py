from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(256), nullable=True, default='default_avatar.png')
    bio = db.Column(db.String(500), nullable=True, default="")
    mood_state = db.Column(db.String(50), nullable=True)
    
    
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    user = db.relationship('User', backref=db.backref('history', lazy=True))


    def __repr__(self):
        return f"<History {self.mood} for User ID {self.user_id}>"
