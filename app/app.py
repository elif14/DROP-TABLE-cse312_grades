from flask import Flask, render_template, make_response, request, redirect
from pymongo import MongoClient
from flask import send_file


app = Flask(__name__)
mongo_client = MongoClient("mongo")
db = mongo_client["cse312-project"]
user_collection = db["chat"]

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
    confirmPassword = request.form.get("confirmPassword")
    # check if the password match
    if password != confirmPassword:
        return "passwords do not match!"
    # return back to homepage
    return redirect("http://localhost:8080/", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)