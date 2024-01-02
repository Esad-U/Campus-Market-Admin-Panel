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



def getUserIdFromToken(token):
    try:
        payload = jwt.decode(token, "campusmarket", algorithms=["HS256"])
        return payload['id']
        
    except Exception as e:
        raise Exception("Invalid Token")

def getUserRoleFromId(id):
    try:
        collection = db[COLLECTION_USER]
        user = collection.find_one({"_id": ObjectId(id)})
        if(user is None):
            raise Exception("User not found")
        return user['role']
    except Exception as e:
        print(e)
        raise Exception("User not found")
        
def makeUserBlocked(userIdToBlock):
    try:
        user_collection = db[COLLECTION_USER]
        print(userIdToBlock)
        result = user_collection.update_one(
            {"_id": ObjectId(userIdToBlock)},
            {"$set": {"blocked": True}}
        )

        if result.modified_count > 0:
            return responseTemplate(200, "User blocked successfully.")
        else:
            return responseTemplate(404, "User not found.")
    except Exception as e:
        return responseTemplate(500, f"Error blocking user: {str(e)}")
def lambda_handler(event, context):
    jwtToken = event["token"]
    userIdToBlock = event["userIdToBlock"]
    try:
        userId = getUserIdFromToken(jwtToken)
        print(userId)
        userRole = getUserRoleFromId(userId)
        print(userRole)
        if(userRole != 'admin'):
            return responseTemplate(401,"Unauthorized")
        return makeUserBlocked(userIdToBlock)    
        
    except Exception as e:
        return responseTemplate(500, dumps({"error": f"Error: {str(e)}"}))
    
    
    
        
