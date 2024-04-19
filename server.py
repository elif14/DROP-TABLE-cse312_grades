import hashlib
import os
import json
import html
from flask import Flask
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
from LineUp.student import student_bp
from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app, \
    url_for, Flask
from pymongo import MongoClient
from flask_socketio import SocketIO, emit

app = Flask(__name__)

client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['on_duty']
student_queue = db['student_queue']
TA_collection = db['TA_collection']
TA_chat_collection = db['TA_chat_collection']
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=os.environ.get('REDIS_URL'), transports=['websocket'])

app.register_blueprint(user_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(ta_bp)
app.register_blueprint(student_bp)

@socketio.on('ClientTAChat')
def socketConnect():
    chatList = []
    allChats = TA_chat_collection.find({})
    for chat in allChats:
        chat.pop("_id")
        chatList.append(chat.get("chat"))
    chatJSON = json.dumps(chatList)
    emit('TAChat', chatJSON)

@socketio.on('ReceiveTAChat')
def socketConnect(chat):
    if (chat.isalnum()):
        curr_auth = request.cookies.get("auth_token")
        if curr_auth is not None:
            hash_obj = hashlib.sha256()
            hash_obj.update(curr_auth.encode())
            hash_obj.digest()
            hash_token = hash_obj.hexdigest()
            if TA_collection.find_one({"auth_token": hash_token}) is not None:
                TA_info = TA_collection.find({"auth_token": hash_token})[0]
                if TA_info is not None:
                    TA_chat = {"chat": TA_info["username"] + ": " + html.escape(chat),
                               "removed": False}
                    TA_chat_collection.insert_one(TA_chat)
                    chatJSON = json.dumps(TA_chat)
                    emit('TAChat', chatJSON)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, allow_unsafe_werkzeug=True, host='0.0.0.0', port=8080, debug=True)
