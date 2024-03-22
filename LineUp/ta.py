from flask import Blueprint

ta_bp = Blueprint('ta_bp', __name__,
    template_folder='templates',
    static_folder='static')