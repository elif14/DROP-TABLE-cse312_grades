from flask import Blueprint

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')


@ta_bp.route('/queue', methods=["POST"])
def ta_enqueue():
    pass


@ta_bp.route('/dequeue', methods=["DELETE"])
def ta_dequeue():
    pass