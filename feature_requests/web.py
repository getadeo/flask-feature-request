from flask import Blueprint

bp = Blueprint('app', __name__, url_prefix='/app')

@bp.route('/')
def index():
    return 'from app'

