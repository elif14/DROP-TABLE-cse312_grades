from flask import Blueprint, render_template

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')

@ta_bp.route('/queue')
def queue_page():
    response = render_template('queue.html')
    return response

@ta_bp.route('/queue', methods=["POST"])
def ta_enqueue():
    pass


@ta_bp.route('/dequeue', methods=["DELETE"])
def ta_dequeue():
    pass