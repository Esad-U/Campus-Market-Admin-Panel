import json
import os 
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import jwt


DB_NAME = "SoftEng"

COLLECTION_CATEGORY = "Category"
COLLECTION_PRODUCT = "Product"
COLLECTION_USER = "User"
COLLECTION_COMMENT = "Comment"

client = MongoClient(host="mongodb+srv://selimyurekligs:Selim12345@cluster0.bvqodo0.mongodb.net/")
db = client[DB_NAME]


def tokenGenerator(user):
    payload={}
    payload['id'] = str(user['_id'])
    encoded_jwt = jwt.encode(payload, "campusmarket", algorithm="HS256")
    del payload['id']
    payload['token'] = encoded_jwt
    return payload


def responseTemplate(statusCode, body):
    return {
                "statusCode": statusCode,
                "body": body,
                "headers": {
                    "Content-Type": "application/json"
                }
            }

def login(email,password):
    collection = db[COLLECTION_USER]
    user = collection.find_one({"email":email, "password": password})

    if(user is None or user == {}):
        return responseTemplate(404,"User not found.")
    elif(user["verified"] == False):
        return responseTemplate(401,"User needs to be verified")    
    else: 
        return responseTemplate(200,dumps(tokenGenerator(user)))

def lambda_handler(event, context):
    email = event["email"]
    password = event["password"]
    return login(email,password)
