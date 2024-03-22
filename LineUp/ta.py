import json

from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app
from pymongo import MongoClient
from LineUp import login

client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']
student_queue = db['student_queue']

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


@ta_bp.route('/ta_display', methods=["GET"])
def ta_display():
    tas = on_duty.find({}, {'_id': 0})
    all_tas = []
    data = {}
    i = 1
    for single_ta in tas:
        all_tas.append(single_ta["username"])
    data["usernames"] = all_tas
    current_app.logger.info(data)
    needed_data = json.dumps(data)
    return jsonify(needed_data)


@ta_bp.route('/dequeue', methods=["POST"])
def ta_dequeue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        username = login.get_username(auth_token)
        on_duty.delete_one({"username": username})
    return redirect('/queue', code=302)


@ta_bp.route('/dequeue_student', methods=["POST"])
def student_dequeue():
    dummy_name = "" # filler variable
    student_queue.update_one({"student_name": dummy_name}, {'$set': {"status": False}})
    pass
