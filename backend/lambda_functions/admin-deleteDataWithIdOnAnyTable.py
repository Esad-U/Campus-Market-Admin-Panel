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


def deleteDataByIdFromCollection(deletedId,categoryName):
    try:
        collection = db[categoryName]
        result = collection.delete_one({"_id": ObjectId(deletedId)})

        if result.deleted_count > 0:
            return responseTemplate(200,dumps(f"Document with ID {deletedId} deleted successfully."))
        else: 
            raise Exception("No data with that id")
        
    except Exception as e:
        return responseTemplate(500,f'Error: {str(e)}')

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
        raise Exception("Error when validate user")

def lambda_handler(event, context):
    collectionName = event["table"]
    deletedId = event["id"]
    jwtToken = event["token"]
    try:
        userId = getUserIdFromToken(jwtToken)
        userRole = getUserRoleFromId(userId)
        if(userRole != 'admin'):
            return responseTemplate(401,"Unauthorized")
        if(collectionName == COLLECTION_PRODUCT or collectionName ==COLLECTION_CATEGORY or collectionName ==COLLECTION_COMMENT or collectionName ==COLLECTION_USER):
            return deleteDataByIdFromCollection(deletedId, collectionName)    
        else:
            return responseTemplate(400,"Bad request for table")
    except Exception as e:
        return responseTemplate(500, dumps({"error": f"Error: {str(e)}"}))
    
    
    
        
