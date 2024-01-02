import os 
import json
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

# SMTP server settings
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SMTP_USERNAME = 'no-reply-campusmarket@outlook.com'
SMTP_PASSWORD = 'Selim12345'

DB_NAME = "SoftEng"
COLLECTION_CATEGORY = "Category"
COLLECTION_PRODUCT = "Product"
COLLECTION_USER = "User"
COLLECTION_COMMENT = "Comment"
client = MongoClient(host="mongodb+srv://selimyurekligs:Selim12345@cluster0.bvqodo0.mongodb.net/")
db = client[DB_NAME]


def generate_verification_code():
    return str(secrets.randbelow(99999)).zfill(5)

def send_verification_email(email, verification_code):
    sender_email = 'no-reply-campusmarket@outlook.com'
    subject = 'Verify Your Email Campus Market'
    link = f'https://tnglgfyhba.execute-api.eu-central-1.amazonaws.com/dev/verifyaccount?email={email}&verification_code={verification_code}'
    body = f'Your verification code link is : {link}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, email, msg.as_string())



def responseTemplate(statusCode, body):
    return {
                "statusCode": statusCode,
                "body": body,
                "headers": {
                    "Content-Type": "application/json"
                }
            }


def verifyEmail(email):
    university_domains = ["itu.edu.tr"]
    _, domain = email.split('@', 1)
    return domain in university_domains

def signup(email, password, name, surname, address):
    collection = db[COLLECTION_USER]

    verificationCode = generate_verification_code()
    isEmailCorrectFormat = verifyEmail(email)
    if(not isEmailCorrectFormat):
        return responseTemplate(401, "Please use your ITU university email.")
    user = {
        "email": email,
        "password": password,
        "name": name,
        "surname": surname,
        "role": "user",
        "created_at": {
            "$timestamp": {
            "t": 1701463163,
            "i": 2
            }
        },
        "blocked": False,
        "verified": False,
        "verificationCode": verificationCode,
        "address": address,
        "rate": -1,
        "products": [],
        "comments": []
    }

    try:
        collection = db[COLLECTION_USER]
        result = collection.insert_one(user)
        send_verification_email(email,verificationCode)
        inserted_user_id = result.inserted_id
        return responseTemplate(200,json.dumps({"message": "User created successfully", "inserted_user_id": str(inserted_user_id)}) )

    except Exception as e:
        return responseTemplate(500,json.dumps({"error": f"Error: {str(e)}"}), )


def lambda_handler(event, context):
    email = event["email"]
    password = event["password"]
    name = event["name"]
    surname = event["surname"]
    address = event["address"]
    
    collection = db[COLLECTION_USER]
    user = collection.find_one({"email":email})
    if(user is None or user == {}):
        return signup(email,password, name, surname, address)
    else: 
        return responseTemplate(400, "Email is already in use.")

