import os 
import json
import smtplib
import secrets
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
client = MongoClient(host="mongodb+srv://selimyurekligs:Selim12345@cluster0.bvqodo0.mongodb.net/")
db = client[DB_NAME]

def lambda_handler(event, context):
    try:
        categories_collection = db[COLLECTION_CATEGORY]

        categories = list(categories_collection.find({}, {"_id": 0, "categoryName": 1}))

        return responseTemplate(200, dumps(categories))
        
    except Exception as e:
        return responseTemplate(500, {"error": f"Error retrieving categories: {str(e)}"})