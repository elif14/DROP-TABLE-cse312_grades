from flask import Blueprint, render_template, make_response, send_file
from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

ta_page_bp = Blueprint('ta_page_bp', __name__, 
                    template_folder = 'templates', 
                    static_folder = 'static')

@ta_page_bp.route('/ta')
def ta_page():
    list_of_TAs = []
    all_tas = TA_collection.find({})
    for ta in all_tas:
        list_of_TAs.append(ta["username"])

    response = render_template('ta.html', list_of_TAs = list_of_TAs)
    response = make_response(response)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@ta_page_bp.route('/static/ta.css')
def ta_css():
    response = send_file('LineUp/static/ta.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

