from flask import Flask, render_template, make_response, request, redirect
from pymongo import MongoClient
from flask import send_file
import string


app = Flask(__name__)
mongo_client = MongoClient("mongo")
db = mongo_client["cse312-project"]
user_collection = db["users"]

@app.route('/')
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


@app.route('/register', methods = ["POST"])
def register():
    # get the form data
    username = request.form.get("username")
    password = request.form.get("password")
    # check if password is secure
    if not password_check(password):
        return "password must be of length 10 with at least 1 number, lowercase letter, and uppercase letter."
    confirmPassword = request.form.get("confirmPassword")
    # check if the password match
    if password != confirmPassword:
        return "passwords do not match!"
    # return back to homepage
    return redirect("http://localhost:8080/", code=302)


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