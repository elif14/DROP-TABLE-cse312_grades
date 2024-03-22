from flask import Blueprint, render_template, make_response, send_file

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')

@ta_bp.route('/queue')
def queue_page():
    response = render_template('queue.html')
    response = make_response(response)
    response.headers['X-Content-Type-Options'] = 'nosniff'
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