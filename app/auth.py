import login
import string
from pymongo import MongoClient
import hashlib
import random

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

def create_auth_token(username):
    auth_token = "".join(random.choices(string.ascii_letters + string.digits, k=20))
    hash_obj = hashlib.sha256()
    hash_obj.update(auth_token.encode)
    hash_obj.digest()
    needed_token = hash_obj.hexdigest()
    TA_collection.update_one({"username": username}, {"$set": {"auth_token": needed_token}})
    return needed_token
