from flask import Flask, render_template
from pymongo import MongoClient
from flask import send_file

app = Flask(__name__)
client = MongoClient("mongo:27017")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/static/style.css')
def sendStyle():
    return send_file('static/style.css')


@app.route('/static/functions.js')
def sendFunctions():
    return send_file('static/functions.js')


@app.route('/static/wonwoo.jpeg')
def sendWonwoo():
    return send_file('static/image.jpg', mimetype='image/jpeg')

@app.route('/signup')
def signup():
    return 'This is a sign up page!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)