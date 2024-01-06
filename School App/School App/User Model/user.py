# user.py
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password, name, profile_picture):
        self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.profile_picture = profile_picture
