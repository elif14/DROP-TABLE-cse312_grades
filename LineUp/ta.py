import html
import json
from datetime import datetime, timedelta
from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app, url_for
from pymongo import MongoClient
from LineUp import login
import hashlib
import datetime


client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']
student_queue = db['student_queue']
TA_collection = db['TA_collection']
TA_chat_collection = db['TA_chat_collection']

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')


@ta_bp.route('/')
def queue_page():
    username = "Guest"
    lstOfAllStudents = []
    lstOfAllTAChats = []
    allStudents = student_queue.find({})
    for eachStudent in allStudents:
        if eachStudent["dequeued"] == False:
            lstOfAllStudents.append(eachStudent["student"])
        elif eachStudent["dequeued"] == True:
            lstOfAllStudents.append(eachStudent["student"] + " has been helped")
    all_TA_chats = TA_chat_collection.find({})
    for each_chat in all_TA_chats:
        if each_chat.get("removed") is False:
            lstOfAllTAChats.append(each_chat.get("chat"))
    #current_app.logger.info(lstOfAllStudents)
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        if user_exist(auth_token):
            username = login.get_username(auth_token)
    response = render_template('homepage.html', username=username, studentQ=lstOfAllStudents, TA_chat=lstOfAllTAChats)
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
        if user_exist(auth_token):
            username = login.get_username(auth_token)
            if on_duty.find_one({"username": username}) is None:
                TA = {"username": username}
                on_duty.insert_one(TA)
    return redirect('/', code=302)


@ta_bp.route('/ta_display', methods=["GET"])
def ta_display():
    tas = on_duty.find({}, {'_id': 0})
    all_tas = []
    for single_ta in tas:
        all_tas.append(single_ta["username"] + "(" + str(datetime.date.today() - timedelta(days=1)) + ")")
    needed_data = json.dumps(all_tas)
    return jsonify(needed_data)

@ta_bp.route('/TA-chat', methods=["GET", "POST"])
def TA_chat():
    if request.method == 'POST':
        if (request.form.get("TA-chat").isalnum()):
            curr_auth = request.cookies.get("auth_token")
            if curr_auth is not None:
                hash_obj = hashlib.sha256()
                hash_obj.update(curr_auth.encode())
                hash_obj.digest()
                hash_token = hash_obj.hexdigest()
                if TA_collection.find_one({"auth_token": hash_token}) is not None:
                    print(TA_collection.find_one({"auth_token": hash_token}))
                    TA_info = TA_collection.find({"auth_token": hash_token})[0]
                    if TA_info is not None:
                        TA_chat = {"chat": TA_info["username"] + ": " + htmlescape(request.form.get("TA-chat")), "removed": False}
                        TA_chat_collection.insert_one(TA_chat)
        return redirect(url_for('ta_bp.queue_page'))


def htmlescape(word):
    word = word.replace('&', '&amp')
    word = word.replace('<', '&lt')
    word = word.replace('>', '&gt')
    return word

#quick question, what do i when someone press the delete button?
#im assuming /dequeue will call /dequeue_student if its authenticated?

@ta_bp.route('/dequeue', methods=["POST"])
def ta_dequeue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        if user_exist(auth_token):
            username = login.get_username(auth_token)
            on_duty.delete_one({"username": username})
    return redirect('/', code=302)

@ta_bp.route('/dequeue_student', methods=["POST"])#not sure how to approach this. i have the studnet name at teh end of the so its like /dequeue_student/"name" prob regx so thats a later prob
def student_dequeue():
    name = request.json['student_name']
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        if user_exist(auth_token):
            student_queue.update_one({"student": name}, {'$set': {"dequeued": True}})
    return redirect('/', code=302)

@ta_bp.route('/remove_TA_chat', methods=["POST"])#not sure how to approach this. i have the studnet name at teh end of the so its like /dequeue_student/"name" prob regx so thats a later prob
def removeChat():
    name = request.json['chat']
    if 'auth_token' in request.cookies:
        curr_auth = request.cookies.get("auth_token")
        if curr_auth is not None:
            hash_obj = hashlib.sha256()
            hash_obj.update(curr_auth.encode())
            hash_obj.digest()
            hash_token = hash_obj.hexdigest()
            if TA_collection.find_one({"auth_token": hash_token}) is not None:
                print(TA_collection.find_one({"auth_token": hash_token}))
                TA_name = TA_collection.find_one({"auth_token": hash_token})["username"]
                TA_chat_search = TA_chat_collection.find_one({"chat": name})
                TA_name_in_chat = TA_chat_search.get("chat").split(":")[0]
                if TA_name_in_chat == TA_name:
                    print(name)
                    TA_chat_collection.update_one({"chat": name}, {'$set': {"removed": True}})
    return redirect('/', code=302)


def user_exist(auth_token):
    hash_obj = hashlib.sha256()
    hash_obj.update(auth_token.encode())
    needed_token = hash_obj.hexdigest()
    if TA_collection.find_one({"auth_token": needed_token}):
        return True
    else:
        return False