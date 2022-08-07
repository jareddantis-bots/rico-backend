from api.notes import *
from flask import Blueprint


bp_notes = Blueprint('notes', __name__)
bp_notes.route('/create', methods=['POST'])(create_note)
bp_notes.route('/list', methods=['GET'])(get_notes)
