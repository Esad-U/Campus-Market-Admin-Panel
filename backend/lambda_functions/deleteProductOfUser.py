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
    
def deleteProductForUser(user_id, product_id):
    try:
        collection = db[COLLECTION_USER]
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$pull": {"products": ObjectId(product_id)}}
        )

        if result.modified_count == 0:
            raise Exception("Product not found for the user")

        # You may want to delete the actual product document from the PRODUCT collection as well
        products_collection = db[COLLECTION_PRODUCT]
        products_collection.delete_one({"_id": ObjectId(product_id)})

        return responseTemplate(200, {"message": "Product deleted successfully"})
    except Exception as e:
        return responseTemplate(500, {"error": f"Error deleting product: {str(e)}"})

def lambda_handler(event, context):
    jwtToken = event["token"]
    deleteProductId = event['deleteProductId']

    try:
        assert jwtToken
        userId = getUserIdFromToken(jwtToken)
        
        deleteProductId = event['deleteProductId']
        return deleteProductForUser(userId, deleteProductId)

    except Exception as e:
        return responseTemplate(500, {"error": f"Error: {str(e)}"})
