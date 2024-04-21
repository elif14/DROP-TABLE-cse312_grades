from flask import Blueprint, render_template, make_response
from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

ta_page_bp = Blueprint('ta_page_bp', __name__, 
                    template_folder = 'templates', 
                    static_folder = 'static')


@ta_page_bp.route('/ta')
def ta_page():
    list_of_TAs = TA_collection.find({})


    response = render_template('ta.html', list_of_TAs = list_of_TAs)
    response = make_response(response)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
