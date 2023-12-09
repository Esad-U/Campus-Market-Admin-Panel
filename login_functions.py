from flask import current_app
from models.user import User


def get_user(email):
    db = current_app.config['dbconfig']
    user = db['users'].find_one({'email': email})

    # ToDo: Create a database script to manage this process

    new_user = User(chats=user['chats'], id=user['_id'], email=user['email'], password=user['password'],
                    name=user['name'], surname=user['surname'], role=user['role'], created_at=user['created_at'],
                    blocked=user['blocked'], verified=user['verified'], verification_code=user['verificationCode'],
                    address=user['address'], rate=user['rate'], profile_img_url=user['profile_image_url'],
                    products=user['products'], comments=user['comments'])

    return new_user
