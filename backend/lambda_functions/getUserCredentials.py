import os 
import json
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

def responseTemplate(statusCode, body):
    return {
                "statusCode": statusCode,
                "body": body,
                "headers": {
                    "Content-Type": "application/json"
                }
            }


def getUserCredentials(_id):
    collection = db[COLLECTION_USER]
    try: 
        user = collection.find_one({"_id": ObjectId(_id)})
        if(user is None):
            return responseTemplate(404, "User not found.")
        del user["password"]
        return responseTemplate(200,dumps(user,indent=2) )

    except Exception as e:
        return responseTemplate(500, json.dumps({"error": f"Error: {str(e)}"}))
def getUserIdFromToken(token):
    try:
        payload = jwt.decode(token, "campusmarket", algorithms=["HS256"])
        return payload['id']
    except Exception as e:
        raise Exception("Error decode")


def lambda_handler(event, context):
    jwt_token =event['token']
    try:
        return getUserCredentials(getUserIdFromToken(jwt_token))
    except Exception as e:
        return responseTemplate(400, dumps({"error": "Error: Invalid token"}))
     
    

