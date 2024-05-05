import hashlib
import os
import json
import html
from datetime import datetime, timedelta
from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app, \
    url_for, Flask
from pymongo import MongoClient
from flask_socketio import SocketIO, emit
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from LineUp.user import user_bp
from LineUp.register import register_bp
from LineUp.login import login_bp
from LineUp.ta import ta_bp
from LineUp.image import image_bp
from LineUp.ta_page import ta_page_bp

app = Flask(__name__)

client = MongoClient("mongo")
db = client["cse312-project"]
TAOnDuty_collection = db['on_duty']
student_queue = db['student_queue']
TA_collection = db['TA_collection']
TA_chat_collection = db['TA_chat_collection']
ip_collection = db['ip_collection']
socketio = SocketIO(app, cors_allowed_origins="*", transports=['websocket'], async_mode='threading')

app.register_blueprint(user_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(ta_bp)
app.register_blueprint(image_bp)
app.register_blueprint(ta_page_bp)

def find_ip_user(ip_address):
    if ip_collection.find_one({"ip": ip_address}) is not None:
        return True
    else:
        return False

def too_many_response():
    response = make_response()
    response.status_code = 429
    return response

@app.before_request
def DOS_prevention():
    ip = request.headers['X-Real-IP']
    ip_found = find_ip_user(ip)
    current_app.logger.info(ip)
    current_time = datetime.now().timetuple()
    if not ip_found:
         ip_collection.insert_one({"ip": ip, "count": 1, "time": current_time})
    if ip_found:
        user = ip_collection.find({"ip": ip})[0]
        banned = not user["count"]
        if not banned:
            if user["count"] >= 50 and (current_time - user["time"]) <= 10:
    #             ban # count = -1 and time is resetted
    #             respond 429
    #        else:
    #             update_record
        if banned:
            if (current_time - user["time"]) < 30:
                return too_many_response()
            if (current_time - user["time"]) >= 30:
                ip_collection.delete_one({"ip": ip})
        




cooldownDict = {}

@socketio.on('connect')
def connect():
    client_id = request.sid
    cooldownDict[client_id] = datetime.now

@socketio.on('TAOnDuty')
def on_duty():
    curr_auth = request.cookies.get("auth_token")
    if curr_auth is not None:
        hash_obj = hashlib.sha256()
        hash_obj.update(curr_auth.encode())
        hash_obj.digest()
        hash_token = hash_obj.hexdigest()
        if TA_collection.find_one({"auth_token": hash_token}) is not None:
            TA_info = TA_collection.find({"auth_token": hash_token})[0]
            if TA_info is not None:
                if TAOnDuty_collection.find_one({"TA": TA_info.get("username")}) is None:
                    TAOnDuty_collection.insert_one({"TA": TA_info.get("username")})
                    TAOnDutyList = []
                    for TA in TAOnDuty_collection.find({}):
                        TAOnDutyList.append(TA.get("TA"))
                    TAOnDutyList = json.dumps(TAOnDutyList)
                    emit('TAOnDutyReceive', TAOnDutyList, broadcast=True)


@socketio.on('populateOnDuty')
def populate_queue():
    TAOnDutyList = []
    for TA in TAOnDuty_collection.find({}):
        TA.pop("_id")
        TAOnDutyList.append(TA.get("TA"))
    TAOnDutyList = json.dumps(TAOnDutyList)
    emit('TAOnDutyReceive', TAOnDutyList, broadcast=True)


@socketio.on('TAOffDuty')
def off_duty():
    curr_auth = request.cookies.get("auth_token")
    if curr_auth is not None:
        hash_obj = hashlib.sha256()
        hash_obj.update(curr_auth.encode())
        hash_obj.digest()
        hash_token = hash_obj.hexdigest()
        if TA_collection.find_one({"auth_token": hash_token}) is not None:
            TA_info = TA_collection.find({"auth_token": hash_token})[0]
            if TA_info is not None:
                TaInCollection = TAOnDuty_collection.find_one({"TA": TA_info.get("username")})
                if TaInCollection is not None:
                    TAOnDuty_collection.delete_one({"TA": TA_info.get("username")})
                    TAOnDutyList = []
                    for TA in TAOnDuty_collection.find({}):
                        TAOnDutyList.append(TA.get("TA"))
                    TAOnDutyList = json.dumps(TAOnDutyList)
                    emit('TAOnDutyReceive', TAOnDutyList, broadcast=True)


@socketio.on('StudentQueue')
def student_enqueue(studentName):
    ID = request.sid
    queueCooldown = timedelta(seconds=10)

    for ID in cooldownDict.keys():
        timeLeft = cooldownDict[ID]
        if (datetime.now() - timeLeft) < queueCooldown:
            return

    studentName = html.escape(studentName + " " + str(datetime.now() - timedelta(days=1) + timedelta(hours=20)))
    if student_queue.find_one({"student": studentName}) is None:
        student_queue.insert_one({"student": studentName, "dequeued": False})
        student = [studentName]
        student = json.dumps(student)
        emit('studentQueue2', student, broadcast=True)

    for ID in cooldownDict.keys():
        cooldownDict[ID] = datetime.now()


@socketio.on('StudentDequeue')
def student_dequeue(id):
    curr_auth = request.cookies.get("auth_token")
    if curr_auth is not None:
        hash_obj = hashlib.sha256()
        hash_obj.update(curr_auth.encode())
        hash_obj.digest()
        hash_token = hash_obj.hexdigest()
        if TA_collection.find_one({"auth_token": hash_token}) is not None:
            TA_info = TA_collection.find({"auth_token": hash_token})[0]
            if TA_info is not None:
                allStudents = student_queue.find({})
                idFinder = 0
                for student in allStudents:
                    if idFinder == int(id):
                        student_queue.delete_one({"student": student.get("student")})
                    idFinder += 1
                Queue = []
                allStudentsInQueue = student_queue.find({})
                for students in allStudentsInQueue:
                    students.pop("_id")
                    Queue.append(students.get("student"))
                QueueJSON = json.dumps(Queue)
                emit('studentQueue', QueueJSON, broadcast=True)


@socketio.on('TADequeue')
def TA_dequeue(id):
    curr_auth = request.cookies.get("auth_token")
    if curr_auth is not None:
        hash_obj = hashlib.sha256()
        hash_obj.update(curr_auth.encode())
        hash_obj.digest()
        hash_token = hash_obj.hexdigest()
        if TA_collection.find_one({"auth_token": hash_token}) is not None:
            TA_info = TA_collection.find({"auth_token": hash_token})[0]
            TAWhoClickedButton = TA_info.get("username")
            if TA_info is not None:
                TAChats = TA_chat_collection.find({})
                TAChat = []
                idFinder = 0
                for TAMessage in TAChats:
                    TAMessage.pop("_id")
                    GivenUsername = id.split("?")[0]
                    Givenid = id.split("?")[1]
                    if idFinder == int(Givenid) and TAWhoClickedButton == GivenUsername:
                        TA_chat_collection.delete_one({"chat": TAMessage.get("chat")})
                    else:
                        TAChat.append(TAMessage.get("chat"))
                    idFinder += 1
                TAChatJSON = json.dumps(TAChat)
                emit('TAChat', TAChatJSON, broadcast=True)

cooldown_duration = timedelta(seconds=10)
@socketio.on('ReceiveTAChat')
def receive_TA_annoucement(chat):
    curr_auth = request.cookies.get("auth_token")
    if curr_auth is not None:
        hash_obj = hashlib.sha256()
        hash_obj.update(curr_auth.encode())
        hash_obj.digest()
        hash_token = hash_obj.hexdigest()
        if TA_collection.find_one({"auth_token": hash_token}) is not None:
            TA_info = TA_collection.find({"auth_token": hash_token})[0]
            if TA_info is not None:
                TA_chat_collection.insert_one({"chat": str(TA_info["username"]) + ": " + str(html.escape(chat)),
                                               "removed": str(False)})
                TA_chat = [str(TA_info["username"]) + ":" + str(html.escape(chat))]
                TA_chat = json.dumps(TA_chat)
                emit('TAChatReceive', TA_chat, broadcast=True)


@socketio.on('populateQueue')
def populate_queue():
    Queue = []
    allStudentsInQueue = student_queue.find({})
    for students in allStudentsInQueue:
        students.pop("_id")
        Queue.append(students.get("student"))
    QueueJSON = json.dumps(Queue)
    emit('studentQueue', QueueJSON, broadcast=True)


@socketio.on('ClientTAChat')
def populate_TA_chat():
    chatList = []
    allChats = TA_chat_collection.find({})
    for chat in allChats:
        chat.pop("_id")
        chatList.append(chat.get("chat"))
    chatJSON = json.dumps(chatList)
    emit('TAChat', chatJSON, broadcast=True)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
