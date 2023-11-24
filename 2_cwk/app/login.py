from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class LoginUser(UserMixin):
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
