import string
from flask import Blueprint, request, redirect
from pymongo import MongoClient
import bcrypt

register_bp = Blueprint('register_bp', __name__,
    template_folder='templates',
    static_folder='static')


client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']


@register_bp.route('/register', methods=["POST"])
def register():
    # get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    # check if the password match
    # if not password_check(password):
    #     return "password must be of length 10 with at least 1 number, lowercase letter, and uppercase letter."
    if password != confirmPassword:
        return redirect('/user', code=302)
    if TA_collection.find_one({"username": username}) is not None:
        return redirect('/user', code=302)
    # salt/hash password, and store in DB
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode(), salt)
    user = {"username": username, 
            "salt": salt, 
            "hashed_password": password}
    TA_collection.insert_one(user)
    return redirect('/user', code=302)


def password_check(password: str):
    if len(password) < 10:
        return False

    num_appear = 0
    upper_appear = 0
    lower_appear = 0
    for c in password:
        if c in string.digits:
            num_appear += 1
        if c in string.ascii_uppercase:
            upper_appear += 1
        if c in string.ascii_lowercase:
            lower_appear += 1

    if num_appear < 1:
        return False
    if upper_appear < 1:
        return False
    if lower_appear < 1:
        return False

    return True