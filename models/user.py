from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def __init__(self, token: str, email: str):
        self.token = token
        self.email = email
        self.active = True

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return self.active
