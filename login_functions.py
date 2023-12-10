from flask import current_app
from models.user import User


def get_user(email):
    db = current_app.config['dbconfig']

    found_user = db.get_user_by_email(email)

    return found_user
