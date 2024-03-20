from flask import Blueprint, render_template, make_response, send_file


homepage_bp = Blueprint('homepage_bp', __name__,
    template_folder='templates',
    static_folder='static')

homepage = '/'

@homepage_bp.route(homepage)
def home():
    response = render_template('index.html')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/style.css')
def sendStyle():
    response = send_file('register/static/style.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/functions.js')
def sendFunctions():
    response = send_file('register/static/functions.js', mimetype='text/javascript')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@homepage_bp.route('/static/image.jpg')
def sendImage():
    response = send_file('register/static/image.jpg', mimetype='image/jpeg')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response