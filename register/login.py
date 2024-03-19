from flask import Flask, request, redirect
from pymongo import MongoClient
import bcrypt
from something import app

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

@app.route('/login', methods=["POST"])
def login():
    username = request.form.get("login_username")
    password = request.form.get("login_password")
    app.logger.info("HAAAAAAAAAAAAAAAA")
    if user_exist(username) and correct_password(username, password):
        # Jessica do your thing; set auth_token
        return redirect('/', code=302)

def user_exist(username: str):
    if TA_collection.find({"usernmae": username}) is not None:
        return True
    else:
        return False
    
def correct_password(username, password):
    user = TA_collection.find({"usernmae": username})
    hashed_password = bcrypt.hashpw(password.encode(), user["salt"])
    if hashed_password is user["password"]:
        return True
    else:
        return False
