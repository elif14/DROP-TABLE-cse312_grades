from flask import Blueprint

ta_bp = Blueprint('example_bp', __name__,
    template_folder='templates',
    static_folder='static')