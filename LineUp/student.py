import json
import queue
from datetime import datetime
from flask import Blueprint, request, redirect, request, url_for
from pymongo import MongoClient

listDictOfStudents = []


student_bp = Blueprint('student_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

client = MongoClient("mongo")
db = client["cse312-project"]
student_queue = db['student_queue']

@student_bp.route('/student', methods=["GET", "POST"])
def student_enqueue():
    date = datetime.now()
    if request.method == 'POST':
        studentName = request.form.get("Name") + date.strftime(" %H:%M")
        studentName = json.dumps(studentName)
        if student_queue.find_one({"student": studentName}) is None:
            student = {"student": studentName, "dequeued": False}
            student_queue.insert_one(student)
        return redirect(url_for('ta_bp.queue_page'))



# MEMO to Alex and Chris
# student_queue table should have at least 2 fields
# 1. student_name (either UBIT or any username)
# 2. True/False value (to indicate whether or not they have been dequeued)
