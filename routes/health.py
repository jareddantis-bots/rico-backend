from flask import Blueprint


bp_health = Blueprint('health', __name__)


@bp_health.route('/health', methods=['GET'])
def health():
    return 'OK'
