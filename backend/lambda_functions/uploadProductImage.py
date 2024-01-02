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
        
def lambda_handler(event, context):
    # Extract parameters from the API Gateway event
    product_id = event['queryStringParameters']['productId']
    request_body = json.loads(event['body'])
    jwtToken = request_body.get('token', '')
        
    try:
        assert jwtToken
        userId = getUserIdFromToken(jwtToken)
        
        # Get the base64-encoded image string from the request body
        image_str = request_body.get('image', '')
        
        if not image_str:
            raise ValueError('Image data is missing in the request body.')
        
        # Decode base64 image string
        image_bytes = base64.b64decode(image_str)
        
        # Convert the image to a PNG format
        image = Image.open(BytesIO(image_bytes))
        output_buffer = BytesIO()
        image.save(output_buffer, format="PNG")
        
        # Upload the image to S3
        s3_key = f"products/{product_id}.png"
        s3.put_object(Body=output_buffer.getvalue(), Bucket=bucket_name, Key=s3_key)
        
        # Return a success response
        return responseTemplate(200, json.dumps({'message': f"Product (with productId={product_id}) image uploaded successfully."}))
        
    except Exception as e:
        return responseTemplate(500, f"Error: {str(e)}")  
