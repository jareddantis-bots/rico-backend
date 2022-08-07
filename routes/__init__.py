from typing import TYPE_CHECKING
from .notes import bp_notes
if TYPE_CHECKING:
    from flask import Flask


URL_PREFIX = '/api/v1'


def install_routes(app: 'Flask'):
    app.register_blueprint(bp_notes, url_prefix=f'{URL_PREFIX}/notes')
