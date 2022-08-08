from api.excluded_threads import *
from flask import Blueprint


bp_excluded_threads = Blueprint('excluded_threads', __name__)
bp_excluded_threads.route('/', methods=['POST'])(add_excluded_thread)
bp_excluded_threads.route('/', methods=['GET'])(get_excluded_threads)
bp_excluded_threads.route('/', methods=['DELETE'])(delete_excluded_thread)
