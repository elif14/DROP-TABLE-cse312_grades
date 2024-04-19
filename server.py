import os

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

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=True)
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
