from api.auth import *
from flask import Blueprint


bp_auth = Blueprint('auth', __name__)
bp_auth.route('/auth/login', methods=['GET'])(discord_oauth2_begin)
bp_auth.route('/auth/callback', methods=['GET'])(discord_oauth2_callback)
