from bson.objectid import ObjectId
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.password = user_data['password']
        self.bio = user_data.get('bio', '')
        self.avatar = user_data.get('avatar', '')

    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    @staticmethod
    def get(user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None
