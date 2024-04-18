import html
import json
from datetime import datetime, timedelta
import logging
from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app, \
    url_for, Flask
from pymongo import MongoClient
from LineUp import login
import hashlib
import datetime
from flask_socketio import SocketIO, emit

app = Flask(__name__)

client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']
student_queue = db['student_queue']
TA_collection = db['TA_collection']
TA_chat_collection = db['TA_chat_collection']
socketio = SocketIO(app, transports=['websocket'])

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
    # current_app.logger.info(lstOfAllStudents)
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        if user_exist(auth_token):
            username = login.get_username(auth_token)
    response = render_template('homepage.html', username=username, studentQ=lstOfAllStudents, TA_chat=lstOfAllTAChats)
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
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
    response = make_response(redirect('/', code=302))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@ta_bp.route('/ta_display', methods=["GET"])
def ta_display():
    tas = on_duty.find({}, {'_id': 0})
    all_tas = []
    for single_ta in tas:
        all_tas.append(single_ta["username"] + "(" + str(datetime.date.today() - timedelta(days=1)) + ")")
    needed_data = json.dumps(all_tas)
    response = make_response(jsonify(needed_data))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@ta_bp.route('/static/functions.js')
def sendFunctions():
    response = send_file('LineUp/static/functions.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@ta_bp.route('/node_modules/socket.io-client/dist/socket.io.js')
def sendSocket():
    response = send_file('node_modules/socket.io-client/dist/socket.io.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@socketio.on('TA-chat1')

def TA_chat():
    # with websockets
    app.logger.info("this part ran 23456789")
    print("testttt2")
    chatList = []
    allChats = TA_chat_collection.find({})
    for chat in allChats:
        chat.pop("_id")
        chatList.append(chat)
    chatJSON = json.dumps(chatList)
    # may need to set the content type to application/json?
    response = make_response(jsonify(chatJSON))
    response.headers["X-Content-Type-Options"] = "nosniff"
    app.logger.info("this part ran 23456789")
    emit('TAChat', chatJSON, broadcast=True)


@socketio.on('connect', namespace='/websocket')
def socketConnect():
    print("connected to websocket")


@socketio.on('disconnect', namespace='/websocket')
def socketDisconnect():
    print("no longer connected to websocket")


# quick question, what do i when someone press the delete button?
# im assuming /dequeue will call /dequeue_student if its authenticated?

@ta_bp.route('/dequeue', methods=["POST"])
def ta_dequeue():
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        if user_exist(auth_token):
            username = login.get_username(auth_token)
            on_duty.delete_one({"username": username})
    response = make_response(redirect('/', code=302))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@ta_bp.route('/dequeue_student', methods=[
    "POST"])  # not sure how to approach this. i have the studnet name at teh end of the so its like /dequeue_student/"name" prob regx so thats a later prob
def student_dequeue():
    name = request.json['student_name']
    if 'auth_token' in request.cookies:
        auth_token = request.cookies["auth_token"]
        if user_exist(auth_token):
            student_queue.update_one({"student": name}, {'$set': {"dequeued": True}})
    response = make_response(redirect('/', code=302))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@ta_bp.route('/remove_TA_chat', methods=[
    "POST"])  # not sure how to approach this. i have the studnet name at teh end of the so its like /dequeue_student/"name" prob regx so thats a later prob
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
                TA_name = TA_collection.find_one({"auth_token": hash_token})["username"]
                TA_chat_search = TA_chat_collection.find_one({"chat": name})
                TA_name_in_chat = TA_chat_search.get("chat").split(":")[0]
                if TA_name_in_chat == TA_name:
                    TA_chat_collection.update_one({"chat": name}, {'$set': {"removed": True}})
    response = make_response(redirect('/', code=302))
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def user_exist(auth_token):
    hash_obj = hashlib.sha256()
    hash_obj.update(auth_token.encode())
    needed_token = hash_obj.hexdigest()
    if TA_collection.find_one({"auth_token": needed_token}):
        return True
    else:
        return False

