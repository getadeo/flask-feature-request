from flask import Blueprint

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    return 'from app'

