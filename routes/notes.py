from api.notes import *
from flask import Blueprint


bp_notes = Blueprint('notes', __name__)
bp_notes.route('/', methods=['POST'])(create_note)
bp_notes.route('/', methods=['GET'])(get_notes)
bp_notes.route('/', methods=['DELETE'])(delete_note)
