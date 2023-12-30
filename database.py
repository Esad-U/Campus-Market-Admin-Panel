from pymongo import MongoClient
from bson import ObjectId
from models.user import User
from datetime import datetime
import requests
import json


class Database:
    def __init__(self, uri: str, url: str, dbname: str):
        self.uri = uri
        self.url = url
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

    def get_users_api(self):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'
        payload = json.dumps({
            "table": "User",
            "page": 1,
            "limit": 30,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def delete_user_api(self, _id):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": "User",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def block_user_api(self, _id):
        url = self.url + '/dev/admin-blockUserWithId'
        payload = json.dumps({
            "userIdToBlock": _id[10:-2],
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def unblock_user_api(self, _id):
        url = self.url + '/dev/admin-unblockUserWithId'
        payload = json.dumps({
            "userIdToUnblock": _id[10:-2],
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

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

    def get_comments_api(self):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'

        payload = json.dumps({
            "table": "Comment",
            "page": 1,
            "limit": 30,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def delete_comment_api(self, _id):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": "Comment",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def delete_comment(self, _id):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['comments'].delete_one({'_id': ObjectId(_id)})

    def get_comment_by_id(self, _id):
        oid = ObjectId(_id)
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            comment = db['comments'].find_one({'_id': oid})

        return_val = (self.get_user_email(comment['comment_to']), self.get_user_email(comment['author']), comment)

        return return_val

    def accept_comment(self, _id):
        oid = ObjectId(_id)
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['comments'].update_one({'_id': oid}, {'$set': {'is_accepted': True}})

    def get_chats_api(self):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'

        payload = json.dumps({
            "table": "Chat",
            "page": 1,
            "limit": 30,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def get_chats(self):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            query = db['chats'].find().sort('updated_at', 1)

            chat_list = []
            for chat in query:
                email_a = db['users'].find_one({'_id': ObjectId(chat['from_id'])})['email']
                email_b = db['users'].find_one({'_id': ObjectId(chat['to_id'])})['email']
                chat_list.append((email_a, email_b, chat))

        return chat_list

    def delete_chat_api(self, _id):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": "Chat",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def delete_chat(self, _id):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['chats'].delete_one({'_id': ObjectId(_id)})

    def get_products_api(self):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'

        payload = json.dumps({
            "table": "Product",
            "page": 1,
            "limit": 30,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def delete_product_api(self, _id):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": "Product",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def get_categories_api(self):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'

        payload = json.dumps({
            "table": "Category",
            "page": 1,
            "limit": 30,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def delete_category_api(self, _id):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": "Category",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def insert_category_api(self, name):
        url = self.url + '/dev/admin-addOrRemoveCategory'

        payload = json.dumps({
            "action": "add_category",
            "categoryName": name,
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY1N2RiMDgxMDM3MDlkNzg5MGNhMDNhOCJ9.v0tVEKUy73_pA3opvG7C4E0wWiaZ-MH8cG3D5223oFg"
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def search_users(self, keyword):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            query = db['users'].find({'email': {'$regex': f'.*{keyword}.*'}})

            if query is not None:
                user_list = [a for a in query]
            else:
                user_list = None

        return user_list

    def search_comments(self, keyword):
        comments = []
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            oids = db['users'].find({'email': {'$regex': f'.*{keyword}.*'}}).distinct('_id')

            if oids:
                for oid in oids:
                    query = db['comments'].find_one({'comment_to': str(oid)})
                    target = db['users'].find_one({'_id': ObjectId(query['comment_to'])})['email']
                    author = db['users'].find_one({'_id': ObjectId(query['author'])})['email']

                    comments.append((target, author, query))
            else:
                print("Not found")

        return comments

    def search_chats(self, keyword):
        chats = []
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            oids = db['users'].find({'email': {'$regex': f'.*{keyword}.*'}}).distinct('_id')

            if oids:
                for oid in oids:
                    query = db['chats'].find_one({'from_id': str(oid)})
                    fr = db['users'].find_one({'_id': ObjectId(query['from_id'])})['email']
                    to = db['users'].find_one({'_id': ObjectId(query['to_id'])})['email']

                    chats.append((fr, to, query))
            else:
                print("Not found")

        return chats

    def search_products(self, keyword):
        prods = []
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            oids = db['users'].find({'email': {'$regex': f'.*{keyword}.*'}}).distinct('_id')

            if oids:
                for oid in oids:
                    query = db['products'].find_one({'user_id': str(oid)})
                    user = db['users'].find_one({'_id': ObjectId(query['user_id'])})['email']
                    category = db['categories'].find_one({'_id': ObjectId(query['category_id'])})['category_name']

                    prods.append((user, category, query))
            else:
                print("Not found")

        return prods

    def search_categories(self, keyword):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            query = db['categories'].find({'category_name': {'$regex': f'.*{keyword}.*'}})

            if query is not None:
                categories_list = [a for a in query]
            else:
                categories_list = None

        return categories_list
