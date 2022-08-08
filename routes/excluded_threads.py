from api.excluded_threads import *
from flask import Blueprint


bp_excluded_threads = Blueprint('excluded_threads', __name__)
bp_excluded_threads.route('/excluded_threads', methods=['POST'])(add_excluded_thread)
bp_excluded_threads.route('/excluded_threads', methods=['GET'])(get_excluded_threads)
bp_excluded_threads.route('/excluded_threads', methods=['DELETE'])(delete_excluded_thread)
bp_excluded_threads.route('/excluded_threads/guilds', methods=['GET'])(get_thread_managed_guilds)
