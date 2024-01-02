import os 
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId


def responseTemplate(statusCode, body):
    return {
                "statusCode": statusCode,
                "body": body,
                "headers": {
                    "Content-Type": "application/json"
                }
            }

DB_NAME = "SoftEng"
COLLECTION_CATEGORY = "Category"
COLLECTION_PRODUCT = "Product"
COLLECTION_USER = "User"
COLLECTION_COMMENT = "Comment"
client = MongoClient(host="mongodb+srv://selimyurekligs:Selim12345@cluster0.bvqodo0.mongodb.net/")
db = client[DB_NAME]

def verify_account(email, verification_code):
    collection = db[COLLECTION_USER]
    user = collection.find_one({"email": email, "verificationCode": verification_code})

    if user:
        collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"verified": True, "verificationCode": None}}
        )
        return responseTemplate(200, "Account verified successfully")
    else:
        return responseTemplate(400, "Invalid user or verification code")


def lambda_handler(event, context):
    email = event["queryStringParameters"]["email"]
    verification_code = event["queryStringParameters"]["verification_code"]

    if email is not None and verification_code is not None:
        # Call your verification logic here
        result = verify_account(email, verification_code)
        return result
    else:
        return responseTemplate(400, "Invalid query parameters")
