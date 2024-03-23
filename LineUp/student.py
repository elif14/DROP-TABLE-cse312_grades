import json
import queue

import flask
from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app, \
    request, url_for
from pymongo import MongoClient
from LineUp import login
import html

from LineUp.ta import ta_bp, queue_page

listDictOfStudents = []


student_bp = Blueprint('student_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

client = MongoClient("mongo")
db = client["cse312-project"]
student_queue = db['student_queue']

@student_bp.route('/student', methods=["GET", "POST"])
def student_enqueue():

    if flask.request.method == 'POST':
        studentName = request.form.get("Name")
        print("student enqueue test")
        print(studentName)
        if student_queue.find_one({"student": studentName}) is None:
            student = {"student": studentName, "dequeued": "False"}
            student_queue.insert_one(student)
            listDictOfStudents.append(student)
            listOfStudentNames= []
            for i in listDictOfStudents:
                listOfStudentNames.append(i.get("student"))
            return redirect(url_for('ta_bp.queue_page', studentQ=listOfStudentNames))



# MEMO to Alex and Chris
# student_queue table should have at least 2 fields
# 1. student_name (either UBIT or any username)
# 2. True/False value (to indicate whether or not they have been dequeued)
