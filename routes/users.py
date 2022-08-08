from api.users import *
from flask import Blueprint


bp_users = Blueprint('users', __name__)
bp_users.route('/', methods=['PUT'])(update_user)
bp_users.route('/', methods=['DELETE'])(delete_user)
