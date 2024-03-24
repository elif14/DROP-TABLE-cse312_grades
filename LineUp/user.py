from flask import Blueprint, render_template, make_response, send_file, request
from pymongo import MongoClient
from LineUp import login

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

user_bp = Blueprint('user_bp', __name__,
    template_folder='templates',
    static_folder='static')



@user_bp.route('/user')
def home():
    username = "Student"
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        username = login.get_username(auth_token)
    response = render_template('user.html', username = username)
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@user_bp.route('/static/user.css')
def sendStyle():
    response = send_file('LineUp/static/user.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@user_bp.route('/static/functions.js')
def sendFunctions():
    response = send_file('LineUp/static/functions.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@user_bp.route('/static/image.jpg')
def sendImage():
    response = send_file('LineUp/static/image.jpg', mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@user_bp.route('/static/picture.jpg')
def sendPicture():
    response = send_file('LineUp/static/picture.jpg', mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response