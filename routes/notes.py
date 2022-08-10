from api.notes import *
from flask import Blueprint


bp_notes = Blueprint('notes', __name__)
bp_notes.route('/notes', methods=['POST'])(create_note)
bp_notes.route('/notes', methods=['GET'])(get_notes)
bp_notes.route('/notes/me', methods=['GET'])(get_my_notes)
bp_notes.route('/notes', methods=['DELETE'])(delete_note)
