import html
import json
from datetime import datetime
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


@ta_bp.route('/')
def queue_page():
    username = "Guest"
    lstOfAllStudents = []
    allStudents = student_queue.find({})
    for eachStudent in allStudents:
        if eachStudent["dequeued"] == False:
            lstOfAllStudents.append(eachStudent["student"])
        elif eachStudent["dequeued"] == True:
            lstOfAllStudents.append(eachStudent["student"] + " has been helped")
    #current_app.logger.info(lstOfAllStudents)
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        username = login.get_username(auth_token)
    response = render_template('homepage.html', username=username, studentQ=lstOfAllStudents)
    return response


@ta_bp.route('/static/homepage.css')
def queue_style():
    response = send_file('LineUp/static/homepage.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@ta_bp.route('/queue', methods=["POST"])
def ta_enqueue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        username = login.get_username(auth_token)
        if on_duty.find_one({"username": username}) is None:
            TA = {"username": username}
            on_duty.insert_one(TA)
    return redirect('/', code=302)


@ta_bp.route('/ta_display', methods=["GET"])
def ta_display():
    tas = on_duty.find({}, {'_id': 0})
    all_tas = []
    date = datetime.now()
    for single_ta in tas:
        all_tas.append(single_ta["username"] + "(" + date.strftime("%d/%m/%y") + ")")
    needed_data = json.dumps(all_tas)
    return jsonify(needed_data)




#quick question, what do i when someone press the delete button?
#im assuming /dequeue will call /dequeue_student if its authenticated?

@ta_bp.route('/dequeue', methods=["POST"])
def ta_dequeue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        username = login.get_username(auth_token)
        on_duty.delete_one({"username": username})
    return redirect('/', code=302)

@ta_bp.route('/dequeue_student', methods=["POST"])#not sure how to approach this. i have the studnet name at teh end of the so its like /dequeue_student/"name" prob regx so thats a later prob
def student_dequeue():
    name = request.json['student_name']
    print("TEST")
    print(name)
    print("<p> cooll <\p> 23:42")
    student_queue.update_one({"student": name}, {'$set': {"dequeued": True}})
    print(student_queue.find_one({"student": name}))
    return redirect('/', code=302)