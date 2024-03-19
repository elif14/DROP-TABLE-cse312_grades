from flask import Flask, render_template, make_response, request, redirect
from pymongo import MongoClient
import hashlib
from auth import create_auth_token
import string

app = Flask(__name__)

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']


@app.route('/logout', methods=["POST"])
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
