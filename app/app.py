import string
from flask import Flask, render_template, make_response, request, redirect
from pymongo import MongoClient
from flask import send_file
import bcrypt


app = Flask(__name__)
client = MongoClient("mongo")
db = client["cse312-project"]
TA_collection = db['TA_collection']

homepage = '/'

@app.route(homepage)
def home():
    response = render_template('index.html')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/static/style.css')
def sendStyle():
    response = send_file('static/style.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/static/functions.js')
def sendFunctions():
    response = send_file('static/functions.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/static/image.jpeg')
def sendImage():
    response = send_file('static/image.jpg', mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@app.route('/register', methods=["POST"])
def register():
    # get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    # check if the password match
    # if not password_check(password):
    #     return "password must be of length 10 with at least 1 number, lowercase letter, and uppercase letter."
    if password != confirmPassword:
        return redirect(homepage, code=302)
    if TA_collection.find_one({"username": username}) is not None:
        return redirect(homepage, code=302)
    # salt/hash password, and store in DB
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(password.encode(), salt)
    TA_collection.insert_one({"username": username, "salt": salt, "password": password})
    # return back to homepage
    return redirect(homepage, code=302)


def password_check(password: str):
    if len(password) < 10:
        return False

    num_appear = 0
    upper_appear = 0
    lower_appear = 0
    for c in password:
        if c in string.digits:
            num_appear += 1
        if c in string.ascii_uppercase:
            upper_appear += 1
        if c in string.ascii_lowercase:
            lower_appear += 1

    if num_appear < 1:
        return False
    if upper_appear < 1:
        return False
    if lower_appear < 1:
        return False

    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
