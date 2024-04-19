import html
import json
import queue
from datetime import datetime, timedelta
from flask import Blueprint, request, redirect, request, url_for
from pymongo import MongoClient
import datetime

listDictOfStudents = []


student_bp = Blueprint('student_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

client = MongoClient("mongo")
db = client["cse312-project"]
student_queue = db['student_queue']

def htmlescape(word):
    word = word.replace('&', '&amp')
    word = word.replace('<', '&lt')
    word = word.replace('>', '&gt')
    return word

# MEMO to Alex and Chris
# student_queue table should have at least 2 fields
# 1. student_name (either UBIT or any username)
# 2. True/False value (to indicate whether or not they have been dequeued)
