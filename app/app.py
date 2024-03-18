import os
from flask import Flask, render_template
from pymongo import MongoClient
from flask import send_file

app = Flask(__name__)
client = MongoClient("mongo:27017")


@app.route('/')
def home():
    css_content = open('static/styles.css').read()

    return css_content, 200, {'Content-Type': 'text/css'}

@app.route('/signup')
def signup():
    return 'This is a sign up page!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
