from flask import current_app, session
from models.user import User


def get_user(email):
    return User(session['token'], email)
