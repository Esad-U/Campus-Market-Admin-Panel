from pymongo import MongoClient
from bson import ObjectId
from models.user import User
from datetime import datetime


class Database:
    def __init__(self, uri: str, dbname: str):
        self.uri = uri
        self.dbname = dbname

    def get_user_by_email(self, email: str):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            user = db['users'].find_one({'email': email})

        if user is not None:
            found_user = User(chats=user['chats'], id=user['_id'], email=user['email'], password=user['password'],
                              name=user['name'], surname=user['surname'], role=user['role'],
                              created_at=user['created_at'], blocked=user['blocked'], verified=user['verified'],
                              verification_code=user['verificationCode'], address=user['address'], rate=user['rate'],
                              profile_img_url=user['profile_image_url'], products=user['products'],
                              comments=user['comments'])
        else:
            found_user = None

        return found_user

    def get_users(self):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            users = db['users'].find().sort('role', 1)

            if users is not None:
                user_list = [a for a in users]
            else:
                user_list = None

        return user_list

    def delete_user(self, _id):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['users'].delete_one({'_id': ObjectId(_id)})

    def insert_user(self, user):
        with MongoClient(self.uri) as client:
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

    def update_password(self, user, new_pw):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]

            db['users'].update_one({'email': user.email}, {'$set': {'password': new_pw}})

    def get_user_email(self, uid):
        oid = ObjectId(uid)
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            email = db['users'].find_one(filter={'_id': oid})['email']

        return email

    def get_comments(self):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            comments = db['comments'].find().sort('is_accepted', 1)

            comment_list = []
            if comments is not None:
                for comment in comments:
                    comment_list.append((self.get_user_email(comment['comment_to']), self.get_user_email(comment['author']),
                                         comment))

        return comment_list

    def delete_comment(self, _id):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['comments'].delete_one({'_id': ObjectId(_id)})
