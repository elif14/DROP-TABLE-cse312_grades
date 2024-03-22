from flask import Blueprint, render_template, send_file, make_response, request, redirect
from pymongo import MongoClient
from LineUp import login

client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']


ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')

@ta_bp.route('/queue')
def queue_page():
    response = render_template('queue.html')
    username = "Guest"
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        username = login.get_username(auth_token)
    response = render_template('queue.html', username=username)
    return response

@ta_bp.route('/static/queue.css')
def queue_style():
    response = send_file('LineUp/static/queue.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@ta_bp.route('/queue', methods=["POST"])
def ta_enqueue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        username = login.get_username(auth_token)
        TA = {"username": username}
        on_duty.insert_one(TA)
    return redirect('/queue', code=302)


@ta_bp.route('/dequeue', methods=["POST"])
def ta_dequeue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        username = login.get_username(auth_token)
        on_duty.delete_one({"username": username})
    return redirect('/queue', code=302)


@ta_bp.route('/dequeue_student', methods=["POST"])
def stud_dequeue():
    pass