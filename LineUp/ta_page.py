from flask import Blueprint, render_template, make_response
from pymongo import MongoClient

client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

ta_page = Blueprint('ta_page', __name__, 
                    template_folder = 'templates', 
                    static_folder = 'static')


@ta_page.route('/ta')
def ta_page():
    list_of_TAs = []
    all_tas = TA_collection.find({})
    for ta in all_tas:
        list_of_TAs.append(ta["username"])

    response = render_template('ta.html', list_of_TAs = list_of_TAs)
    response = make_response(response)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
