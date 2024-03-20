from flask import Blueprint, request, redirect, current_app
from pymongo import MongoClient
import bcrypt
import hashlib
import string
import random

login_bp = Blueprint('login_bp', __name__,
    template_folder='templates',
    static_folder='static')

 
client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

@login_bp.route('/login', methods=["POST"])
def login():
    username = request.form.get("login_username")
    password = request.form.get("login_password")
    if user_exist(username) and correct_password(username, password):
        current_app.logger.info("CREATING AUTH_TOKEN")
        auth_token = create_auth_token(username)
        response = redirect('/', code=302)
        response.set_cookie("auth_token", value=auth_token, max_age=3600, httponly=True)
        response.headers["X-Content-Type-Options"] = "no-sniff"
        return response
    else:
        current_app.logger.info("REDIRECTING TO HOMEPAGE")
        # maybe redirect them to wrong password or error page
        return redirect('/', code=302)

@login_bp.route('/logout', methods=["POST"])
def logout():
    curr_auth = request.cookies["auth_token"]
    new_user = ""
    hash_obj = hashlib.sha256()
    hash_obj.update(curr_auth.encode())
    hash_obj.digest()
    hash_token = hash_obj.hexdigest()
    data_info = TA_collection.find({"auth_token": hash_token}, {"_id": 0})
    for info in data_info:
        # probably what's of objectID type
        new_user = str(info["username"])
    new_auth = create_auth_token(new_user)
    response = redirect("/", code=302)
    response.delete_cookie("auth_token", path="/", domain=None)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

def user_exist(username: str):
    if TA_collection.find({"username": username}) is not None:
        return True
    else:
        return False
    
def correct_password(username, password):
    user = TA_collection.find({"username": username}, {'_id': 0})[0]
    current_app.logger.info(user)
    hashed_password = bcrypt.hashpw(password.encode(), user["salt"])
    current_app.logger.info(hashed_password)
    current_app.logger.info(user["hashed_password"])
    if hashed_password == user["hashed_password"]:
        return True
    else:
        return False

def create_auth_token(username):
    auth_token = "".join(random.choices(string.ascii_letters + string.digits, k=20))
    current_app.logger.info("ENTERED CREATE_AUTH_TOKEN")
    current_app.logger.info(auth_token)
    hash_obj = hashlib.sha256()
    hash_obj.update(auth_token.encode())
    hash_obj.digest()
    needed_token = hash_obj.hexdigest()
    TA_collection.update_one({"username": username}, {"$set": {"auth_token": auth_token}})
    return needed_token
