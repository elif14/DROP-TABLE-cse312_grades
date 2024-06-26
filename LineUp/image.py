from flask import Blueprint, request, current_app, redirect, send_file, make_response
from pymongo import MongoClient
import random
import hashlib

image_bp = Blueprint('image_bp', __name__,
    template_folder='templates',
    static_folder='static')

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

@image_bp.route('/profile-upload', methods=['POST'])
def image_upload():
    if request.method == 'POST':
        curr_auth = request.cookies.get("auth_token")
        if curr_auth is not None:
            hash_obj = hashlib.sha256()
            hash_obj.update(curr_auth.encode())
            hash_obj.digest()
            hash_token = hash_obj.hexdigest()
            data_info = TA_collection.find({"auth_token": hash_token}, {"_id": 0})
            for single_ta in data_info:
                filename = request.files["upload"].filename
                new_image = ""
                if "jpg" in filename:
                    filename = "LineUp/static/" + single_ta["username"] + ".jpg"
                    new_image = "<img src=" + filename + ">"
                TA_collection.update_one({"username": single_ta["username"]}, {"$set": {"image_tag": new_image}})
                with open(filename, "wb") as pro_img:
                    pro_img.write(request.files["upload"].read())
        response = redirect('/user', code=302)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

@image_bp.route('/LineUp/static/<file_name>')
def serve_profile_image(file_name):
    current_app.logger.info("server_profile_image called")
    file_name = file_name.replace("/", "")
    response = send_file('LineUp/static/'+file_name, mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response