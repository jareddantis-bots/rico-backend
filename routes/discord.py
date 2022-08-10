from api.discord import *
from flask import Blueprint


bp_discord = Blueprint('discord', __name__)
bp_discord.route('/discord/me', methods=['GET'])(get_user_details)
