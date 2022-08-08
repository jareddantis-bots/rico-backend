from api.guilds import *
from flask import Blueprint


bp_guilds = Blueprint('guilds', __name__)
bp_guilds.route('/guilds', methods=['POST'])(add_guild)
bp_guilds.route('/guilds', methods=['GET'])(get_guild)
bp_guilds.route('/guilds', methods=['PUT'])(update_guild)
bp_guilds.route('/guilds', methods=['DELETE'])(delete_guild)
