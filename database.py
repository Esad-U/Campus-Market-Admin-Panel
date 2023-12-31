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

    def admin_login(self, email, password):
        url = self.url + '/dev/admin-login'

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response_j = requests.request("POST", url, headers=headers, data=payload).json()

        sc = response_j['statusCode']

        if sc == 200:
            return sc, json.loads(response_j['body'])
        else:
            return sc, response_j['body']

    def get_all_data_from_table(self, table, token):
        url = self.url + '/dev/admin-getAllDataFromAnyTable'
        payload = json.dumps({
            "table": table,
            "token": token,
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        parsed_body = json.loads(response.json()['body'])

        # Access the 'data' key to get the list of elements
        data_list = json.loads(parsed_body['data'])

        return data_list

    def delete_data_from_table(self, _id, table, token):
        url = self.url + '/dev/admin-deleteDataWithIdOnAnyTable'
        payload = json.dumps({
            "id": _id[10:-2],
            "table": table,
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def block_user_api(self, _id, token):
        url = self.url + '/dev/admin-blockUserWithId'
        payload = json.dumps({
            "userIdToBlock": _id[10:-2],
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def unblock_user_api(self, _id, token):
        url = self.url + '/dev/admin-unblockUserWithId'
        payload = json.dumps({
            "userIdToUnblock": _id[10:-2],
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode']

    def update_password(self, user, new_pw):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]

            db['users'].update_one({'email': user.email}, {'$set': {'password': new_pw}})

    def verify_comment_api(self, _id, token):
        url = self.url + '/dev/admin-verifyCommentAndUpdateRate'

        payload = json.dumps({
            "commentId": _id[10:-2],
            "token": token
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()['statusCode'], response.json()['body']

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

    def delete_chat(self, _id):
        with MongoClient(self.uri) as client:
            db = client[self.dbname]
            db['chats'].delete_one({'_id': ObjectId(_id)})

    def insert_category_api(self, name, token):
        url = self.url + '/dev/admin-addOrRemoveCategory'

        payload = json.dumps({
            "action": "add_category",
            "categoryName": name,
            "token": token
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
