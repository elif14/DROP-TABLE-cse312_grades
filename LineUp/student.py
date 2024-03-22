from flask import Blueprint
from pymongo import MongoClient


client = MongoClient("mongo")
db = client["cse312-project"]
on_duty = db['student_queue']

student_bp = Blueprint('student_bp', __name__,
    template_folder='templates',
    static_folder='static')
'''
MEMO to Alex and Chris
"student_queue" table should have at least 2 fields
1. student name (either UBIT or any username)
2. True/False value (to indicate whether or not they have been dequeued)

We can not actually delete student off the queue since handout states that 
"All interactions should be visible to all [authenticated] users (You decide if guests can see interactions)."
which means we can't get rid of their name but change it to light gray or make
a cross line to their name to show that interaction have made by TA (authenticated user)

So when you guys insert a student into "student_queue" table, not only include their username
but also include True value so that we can later updatae that field when TA dequeue student
'''