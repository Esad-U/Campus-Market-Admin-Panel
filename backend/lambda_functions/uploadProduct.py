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

def getUserFromId(id):
    try:
        collection = db[COLLECTION_USER]
        user = collection.find_one({"_id": ObjectId(id)})
        if(user is None):
            raise Exception("User not found")
        return user
    except Exception as e:
        raise Exception("User not found")
def getCategoryIdFromName(categoryName):
    categoryCollection = db[COLLECTION_CATEGORY]
    return categoryCollection.find_one({"categoryName": categoryName})['_id'].__str__()

def lambda_handler(event, context):

    productCollection = db[COLLECTION_PRODUCT]
    userCollection = db[COLLECTION_USER]
    try:
        jwtToken = event["token"]
        title = event["title"]
        description = event["description"]
        category = event["category"]
        price = event["price"]
        print(event)
        assert jwtToken
        assert title
        assert description
        assert category
        assert price
        categoryCollection = db[COLLECTION_CATEGORY]
        categoryId = getCategoryIdFromName(category)
        print(categoryId)
        if(not categoryId): 
            return responseTemplate(404, "Not a valid category")
            
        isSold = False
        newProduct = {
            "title":title,
            "description": description,
            "price":price,
            "categoryId" : ObjectId(categoryId),
            "isSold" : isSold
        }
    
        userId = getUserIdFromToken(jwtToken)
        newProduct['userId'] = ObjectId(userId)
        result_product_insert = productCollection.insert_one(newProduct)
        if(result_product_insert.inserted_id):
            product_id = result_product_insert.inserted_id
            result_user_update = userCollection.update_one(
                {"_id": ObjectId(userId)},
                {"$push": {"products": ObjectId(product_id)}}
            )
            if result_user_update.modified_count > 0:
                return responseTemplate(200,"Product added succesfully.")
            else:
                raise Exception("User not found or no update needed.")
        else:
            raise Exception("Couldn't be inserted.")
            
    except Exception as e:
        return responseTemplate(500, f"Error: {str(e)}")
    




    
    
    
        
