import flask

app = flask.Flask("myApp")

@app.route('/')
def home(name):
    cookies = flask.request.cookies
    return f"hello {name}"