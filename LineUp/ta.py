import html
import json
import os
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

@app.before_request
def something():
    return DOS.DOS_prevention()

client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']
student_queue = db['student_queue']
TA_collection = db['TA_collection']
TA_chat_collection = db['TA_chat_collection']
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=os.environ.get('REDIS_URL'), transports=['websocket'])

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


# quick question, what do i when someone press the delete button?
# im assuming /dequeue will call /dequeue_student if its authenticated?


def user_exist(auth_token):
    hash_obj = hashlib.sha256()
    hash_obj.update(auth_token.encode())
    needed_token = hash_obj.hexdigest()
    if TA_collection.find_one({"auth_token": needed_token}):
        return True
    else:
        return False