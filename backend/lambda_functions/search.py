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
        
def getAllProductsSortedAndPaginated(page, limit):
    try:
        products_collection = db[COLLECTION_PRODUCT]
        users_collection = db[COLLECTION_USER]

        pipeline = [
            {
                "$lookup": {
                    "from": COLLECTION_USER,
                    "localField": "userId",
                    "foreignField": "_id",
                    "as": "user_info"
                }
            },
            {
                "$unwind": "$user_info"
            },
            {
                "$sort": {
                    "user_info.rate": -1  # Sort by user's rate in descending order
                }
            },
            {
                "$skip": (page - 1) * limit
            },
            {
                "$limit": limit
            },
            {
                "$project": {
                    "_id": 1,
                    "title": 1,
                    "description": 1,
                    "price": 1,
                    "categoryId": 1,
                    "isSold": 1,
                    "user": {
                        "name": "$user_info.name",
                        "rate": "$user_info.rate",
                        "surname": "$user_info.surname"
                    }
                }
            }
        ]
        # Execute the aggregation pipeline
        products = list(products_collection.aggregate(pipeline))
        return responseTemplate(200, dumps(products))
    except Exception as e:
        return responseTemplate(500, f"Error retrieving products: {str(e)}")

def lambda_handler(event, context):
    jwtToken = event["token"]
    print(jwtToken)
    try:
        assert jwtToken
        userId = getUserIdFromToken(jwtToken)
        page = event['page'] or 1
        limit = event['limit'] or 10
        return getAllProductsSortedAndPaginated(page, limit)

    except Exception as e:
        return responseTemplate(500, f"Error: {str(e)}")
