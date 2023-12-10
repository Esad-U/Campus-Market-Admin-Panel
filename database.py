from pymongo import MongoClient
from models.user import User

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
            found_user = User(chats=user['chats'], id=user['_id'], email=user['email'], password=user['password'],
                    name=user['name'], surname=user['surname'], role=user['role'], created_at=user['created_at'],
                    blocked=user['blocked'], verified=user['verified'], verification_code=user['verificationCode'],
                    address=user['address'], rate=user['rate'], profile_img_url=user['profile_image_url'],
                    products=user['products'], comments=user['comments'])
        else:
            found_user = None

        return found_user
