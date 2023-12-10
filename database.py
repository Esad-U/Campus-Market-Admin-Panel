from pymongo import MongoClient
from bson import ObjectId
from models.user import User
from datetime import datetime

class Database:
    def __init__(self, url: str, port: int, dbname: str):
        self.url = url
        self.port = port
        self.dbname = dbname

    def get_user_by_email(self, email: str):
        with MongoClient(host=self.url, port=self.port) as client:
            db = client[self.dbname]
            user = db['users'].find_one({'email': email})

        if user is not None:
            found_user = User(chats=user['chats'], _id=user['_id'], email=user['email'], password=user['password'],
                              name=user['name'], surname=user['surname'], role=user['role'],
                              created_at=user['created_at'], blocked=user['blocked'], verified=user['verified'],
                              verification_code=user['verificationCode'], address=user['address'], rate=user['rate'],
                              profile_img_url=user['profile_image_url'], products=user['products'],
                              comments=user['comments'])
        else:
            found_user = None

        return found_user

    def get_users(self):
        with MongoClient(host=self.url, port=self.port) as client:
            db = client[self.dbname]
            users = db['users'].find()

            if users is not None:
                user_list = [a for a in users]
            else:
                user_list = None

        return user_list

    def delete_user(self, _id):
        with MongoClient(host=self.url, port=self.port) as client:
            db = client[self.dbname]
            db['users'].delete_one({'_id': ObjectId(_id)})

    def insert_user(self, user):
        with MongoClient(host=self.url, port=self.port) as client:
            db = client[self.dbname]
            inserted_id = db['users'].insert_one({
                'chats': user.chats,
                'email': user.email,
                'password': user.password,
                'name': user.name,
                'surname': user.surname,
                'role': user.role,
                'created_at': user.created_at,
                'blocked': user.blocked,
                'verified': user.verified,
                'verificationCode': user.verification_code,
                'address': user.address,
                'rate': user.rate,
                'profile_image_url': user.profile_img_url,
                'products': user.products,
                'comments': user.comments
            })

        return inserted_id
