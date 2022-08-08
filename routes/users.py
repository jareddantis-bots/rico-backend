from api.users import *
from flask import Blueprint


bp_users = Blueprint('users', __name__)
bp_users.route('/users', methods=['PUT'])(update_user)
bp_users.route('/users', methods=['DELETE'])(delete_user)
