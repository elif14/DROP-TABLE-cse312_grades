import json

from flask import Blueprint, render_template, send_file, make_response, request, redirect, jsonify, current_app
from pymongo import MongoClient
from LineUp import login
import html

student_bp = Blueprint('student_bp', __name__,
                       template_folder='templates',
                       static_folder='static')

client = MongoClient("mongo")
db = client["cse312-project"]
student_queue = db['student_queue']

@student_bp.route('/student', methods=["POST"])
def student_enqueue():
    student_name = request.form.get("Name")
    if student_queue.find_one({"student": student_name}) is None:
        student = {"student": student_name, "dequeued": "False"}
        student_queue.insert_one(student)
    return redirect('/queue', code=302)

@student_bp.route('/student-display', methods=["GET"])
def student_display(): # need to figure out a way to access json

    return redirect('/queue', code=302)

# MEMO to Alex and Chris
# student_queue table should have at least 2 fields
# 1. student_name (either UBIT or any username)
# 2. True/False value (to indicate whether or not they have been dequeued)
