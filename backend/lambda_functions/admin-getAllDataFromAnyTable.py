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

def getAllFromCollection(categoryName, page=1, limit=10):
    try:
        if(page is None):
            page = 1
        if(limit is None):
            limit = 10
        collection = db[categoryName]
        
        # Calculate the starting index for pagination
        start_index = (page - 1) * limit
        
        # Fetch data for the specified page and limit
        result = collection.find({}).skip(start_index).limit(limit)
        
        # Get the total count of documents in the collection
        total_count = collection.count_documents({})
        
        # Calculate the total number of pages
        total_pages = (total_count + limit - 1) // limit
        
        # Prepare the response body
        response_body = {
            "data": dumps(result),
            "page": page,
            "limit": limit,
            "totalPages": total_pages,
            "totalCount": total_count
        }
        print(response_body)
        return responseTemplate(200, dumps(response_body))
    except Exception as e:
        return responseTemplate(500, f'Error: {str(e)}')

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
        if user is None:
            raise Exception("User not found")
        return user['role']
    except Exception as e:
        raise Exception("Error when validating user")

def lambda_handler(event, context):
    collectionName = event["table"]
    jwtToken = event["token"]
    page = event["page"]  # Get the page parameter, default to 1 if not provided
    limit = event["limit"]  # Get the limit parameter, default to 10 if not provided
    
    try:
        userId = getUserIdFromToken(jwtToken)
        userRole = getUserRoleFromId(userId)
        
        if userRole != 'admin':
            return responseTemplate(401, "Unauthorized")
        
        if collectionName == COLLECTION_PRODUCT or collectionName == COLLECTION_CATEGORY or collectionName == COLLECTION_COMMENT or collectionName == COLLECTION_USER:
            return getAllFromCollection(collectionName, page, limit)
        else:
            return responseTemplate(400, "Bad request for table")
    except Exception as e:
        return responseTemplate(500, dumps({"error": f"Error: {str(e)}"}))
