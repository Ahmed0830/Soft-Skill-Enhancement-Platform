from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
load_dotenv(".env")
uri = os.getenv("mongo_uri")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["hex"]
collection = db["user_details"]

def insert_user(email, password, name="", age=0, bio=""):
    hashed_password = generate_password_hash(password)
    collection.insert_one(
        {
            "email": email,
            "password": hashed_password,
            "name": name,
            "age": age,
            "bio": bio
        }
    )
def get_user(username):
    return collection.find_one({"email": username})

def check_user(email, password):
    user = collection.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return True
    return False

def update_user(email, name, age, bio, profile_pic_data=None):
    update_fields = {"name": name, "age": age, "bio": bio}
    if profile_pic_data:
        update_fields["profile_pic"] = profile_pic_data
    collection.update_one(
        {"email": email},
        {"$set": update_fields}
    )

def get_details(key, data):
    if data:
        return key[data]
def get_leaderboard():
    leaderboard = list(collection.find({"name": {"$ne": ""}, "daily_score": {"$exists": True}}, {'name': 1, 'daily_score': 1, '_id': 0}).sort('daily_score', DESCENDING))
    return leaderboard
