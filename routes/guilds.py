from api.guilds import *
from flask import Blueprint


bp_guilds = Blueprint('guilds', __name__)
bp_guilds.route('/', methods=['PUT'])(update_guild)
bp_guilds.route('/', methods=['DELETE'])(delete_guild)
