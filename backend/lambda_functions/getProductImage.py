import json
import boto3
import base64
from io import BytesIO
from PIL import Image

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import jwt

s3 = boto3.client('s3')
bucket_name = 'campusmarket'

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

def getUserImageFromS3(product_id):
    # accessing object from bucket
    s3_key = f"products/{product_id}.png"
    response = s3.get_object(Bucket=bucket_name, Key=s3_key)
    image_data = response['Body'].read()

    # Convert the image to base64
    base64_image = base64.b64encode(image_data).decode('utf-8')
    return base64_image

def lambda_handler(event, context):
    # Extract parameters from the API Gateway event
    product_id = event['queryStringParameters']['productId']
    jwtToken = event['queryStringParameters']['token']
        
    try:
        assert jwtToken
        userId = getUserIdFromToken(jwtToken)
        
        # Get the image from S3
        base64_image = getUserImageFromS3(product_id)
        
        # Return a success response
        response_body = {'message': f"Product (with userId={product_id}) image retrieved successfully.", 'image': base64_image}
        return responseTemplate(200, json.dumps(response_body))
        
    except Exception as e:
        return responseTemplate(500, f"Error: {str(e)}")  
