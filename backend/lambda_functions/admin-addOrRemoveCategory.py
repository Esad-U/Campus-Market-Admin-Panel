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
        print(e)
        raise Exception("Invalid Token")

def getUserRoleFromId(id):
    try:
        collection = db[COLLECTION_USER]
        user = collection.find_one({"_id": ObjectId(id)})
        if(user is None):
            raise Exception("User not found")
        return user['role']
    except Exception as e:
        raise Exception("User not found")
        
def addCategory(categoryName):
    try:
        # Assuming you have a 'Category' collection
        category_collection = db[COLLECTION_CATEGORY]

        # Check if the category already exists
        existing_category = category_collection.find_one({"categoryName": categoryName})
        if existing_category:
            return responseTemplate(400, f"Category '{categoryName}' already exists.")

        # Add the category to the 'Category' collection
        category_collection.insert_one({"categoryName": categoryName})

        return responseTemplate(200, f"Category '{categoryName}' added successfully.")
    except Exception as e:
        return responseTemplate(500,  f"Error adding category: {str(e)}")


def removeCategory(categoryName):
    try:
        category_collection = db[COLLECTION_CATEGORY]

        result = category_collection.delete_one({"categoryName": categoryName})

        if result.deleted_count > 0:
            return responseTemplate(200, f"Category '{categoryName}' removed successfully.")
        else:
            return responseTemplate(404, f"Category '{categoryName}' not found.")
    except Exception as e:
        return responseTemplate(500, f"Error removing category: {str(e)}")


def lambda_handler(event, context):
    assert event['action']
    action = event['action']

    if action == 'add_category':
        categoryName = event['categoryName']
        return addCategory(categoryName)
    elif action == 'remove_category':
        categoryName = event['categoryName']
        return removeCategory(categoryName)
    else:
        return responseTemplate(400, "Invalid action.")


def lambda_handler(event, context):
    
    jwtToken = event["token"]
    action = event['action']
    assert jwtToken
    assert action
    
    try:
        userId = getUserIdFromToken(jwtToken)
        userRole = getUserRoleFromId(userId)
        if(userRole != 'admin'):
            return responseTemplate(401,"Unauthorized")
        if action == 'add_category':
            categoryName = event['categoryName']
            return addCategory(categoryName)
        elif action == 'remove_category':
            categoryName = event['categoryName']
            return removeCategory(categoryName)
        else:
            return responseTemplate(400, "Invalid action.")
    except Exception as e:
        return responseTemplate(500, dumps({"error": f"Error: {str(e)}"}))
    
    
    
        
