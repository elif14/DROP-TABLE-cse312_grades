import os
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongo:27017")

@app.route('/')
def home():
	return "This is a homepage!"

@app.route('/signup')
def signup():
    return 'This is a sign up page!'
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)