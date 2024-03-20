from flask import Blueprint, render_template, make_response, send_file, request
from pymongo import MongoClient
from LineUp import login

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

homepage_bp = Blueprint('homepage_bp', __name__,
    template_folder='templates',
    static_folder='static')

homepage = '/'

@homepage_bp.route(homepage)
def home():
    username = "Guest"
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        username = login.get_username(auth_token)
    response = render_template('index.html', username = username)
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/style.css')
def sendStyle():
    response = send_file('LineUp/static/style.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/functions.js')
def sendFunctions():
    response = send_file('LineUp/static/functions.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/image.jpg')
def sendImage():
    response = send_file('LineUp/static/image.jpg', mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response