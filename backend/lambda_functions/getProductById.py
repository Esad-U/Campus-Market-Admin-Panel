import os 
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId


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


#Products
def getProductById(_id):
    collection = db[COLLECTION_PRODUCT]
    try: 
        product = collection.find_one({"_id": ObjectId(_id)})
        if(product is None):
            return responseTemplate(404,"Product Not Found")
        return responseTemplate(200,dumps(product))

    except Exception as e:
        return responseTemplate(500,json.dumps({"error": f"Error: {str(e)}"}))


def lambda_handler(event, context):
    return getProductById(event["id"])
