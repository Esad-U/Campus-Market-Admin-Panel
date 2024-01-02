import os 
import json
import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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


# SMTP server settings
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
SMTP_USERNAME = 'no-reply-campusmarket@outlook.com'
SMTP_PASSWORD = 'Selim12345'

DB_NAME = "SoftEng"
COLLECTION_USER = "User"
client = MongoClient(host="mongodb+srv://selimyurekligs:Selim12345@cluster0.bvqodo0.mongodb.net/")
db = client[DB_NAME]

def generate_reset_token():
    return str(secrets.randbelow(99999)).zfill(5)

def send_password_reset_email(email, reset_token):
    sender_email = 'no-reply-campusmarket@outlook.com'
    subject = 'Password Reset Campus Market'
    link = f'https://tnglgfyhba.execute-api.eu-central-1.amazonaws.com/dev/resetpassword?email={email}&reset_token={reset_token}'
    body = f'Your token to reset your password: {reset_token}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    print(msg)
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(sender_email, email, msg.as_string())
        print("sended")

def reset_password(email, reset_token, new_password):
    collection = db[COLLECTION_USER]
    user = collection.find_one({"email": email, "reset_token": reset_token})
    if user:
        # Update the user's password and remove the reset_token
        collection.update_one(
            {"email": email},
            {"$set": {"password": new_password}, "$unset": {"reset_token": ""}}
        )
        return responseTemplate(200,  "Password reset successful.")
    else:
        return responseTemplate(404, "Invalid email or reset token.")

def lambda_handler(event, context):
    print(event)
    if 'action' in event:
        action = event['action']

        if action == 'forgot_password':
            email = event['email']
            user = db[COLLECTION_USER].find_one({"email": email})

            if user:
                reset_token = generate_reset_token()
                print(reset_token)

                db[COLLECTION_USER].update_one({"email": email}, {"$set": {"reset_token": reset_token}})
                print(reset_token)

                send_password_reset_email(email, reset_token)
                return responseTemplate(200,"Password reset email sent successfully.")
            else:
                return responseTemplate(404,"User not found.")
        elif action == 'reset_password':
            email = event['email']
            reset_token = event['reset_token']
            new_password = event['new_password']

            result = reset_password(email, reset_token, new_password)
            return result
        else:
            return responseTemplate(400, "Invalid action.")
    else:
        return responseTemplate(400, "Action not specified.")
