from flask import Blueprint, render_template, send_file, make_response, request
from LineUp import login

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')

@ta_bp.route('/queue')
def queue_page():
    response = render_template('queue.html')
    username = "Guest"
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get("auth_token")
        username = login.get_username(auth_token)
    response = render_template('queue.html', username=username)
    return response

@ta_bp.route('/static/queue.css')
def queue_style():
    response = send_file('LineUp/static/queue.css', mimetype='text/css')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@ta_bp.route('/queue', methods=["POST"])
def ta_enqueue():
    pass


@ta_bp.route('/dequeue', methods=["DELETE"])
def ta_dequeue():
    pass