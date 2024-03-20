from flask import Blueprint, request, redirect, current_app
from pymongo import MongoClient
import bcrypt

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
    current_app.logger.info(username)
    current_app.logger.info(password)
    if user_exist(username) and correct_password(username, password):
        # Jessica do your thing; set auth_token
        return redirect('/', code=302)
    else:
        # maybe redirect them to wrong password or error page
        return redirect('/', code=302)

def user_exist(username: str):
    if TA_collection.find({"usernmae": username}) is not None:
        return True
    else:
        return False
    
def correct_password(username, password):
    user = TA_collection.find({"username": username})[0]
    hashed_password = bcrypt.hashpw(password.encode(), user["salt"])
    if hashed_password is user["hashed_password"]:
        return True
    else:
        return False
