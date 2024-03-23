from flask import Blueprint
from pymongo import MongoClient


client = MongoClient("mongo")
db = client["cse312-project"]
student_queue = db['student_queue']

student_bp = Blueprint('student_bp', __name__,
    template_folder='templates',
    static_folder='static')
'''
MEMO to Alex and Chris
"student_queue" table should have at least 2 fields
1. student_name (either UBIT or any username)
2. True/False value (to indicate whether or not they have been dequeued)

Example of what is going into database "student_queue" table:
{"student_name": "Megan", "status": True}

We can not actually delete student off the queue since handout states that 
"All interactions should be visible to all [authenticated] users (You decide if guests can see interactions)."
which means we can't get rid of their name but change it to light gray or make
a cross line to their name to show that interaction have made by TA (authenticated user)

So when you guys insert a student into "student_queue" table, not only include their username
but also include True value so that we can later updatae that field when TA dequeue student

############################################################################
Also, please make a delete button next to student's name in the queue so that
it requests POST to /dequeue_student. 
Then, our "student_dequeue" function in ta.py in line 68 will take care of deleting it.
We didn't fully finished the function since there is no student's post yet.
############################################################################
'''