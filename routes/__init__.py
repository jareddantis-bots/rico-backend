from typing import TYPE_CHECKING
from .excluded_threads import bp_excluded_threads
from .guilds import bp_guilds
from .notes import bp_notes
from .users import bp_users
if TYPE_CHECKING:
    from flask import Flask


URL_PREFIX = '/api/v1'


def install_routes(app: 'Flask'):
    app.register_blueprint(bp_excluded_threads, url_prefix=f'{URL_PREFIX}/excluded_threads')
    app.register_blueprint(bp_guilds, url_prefix=f'{URL_PREFIX}/guilds')
    app.register_blueprint(bp_notes, url_prefix=f'{URL_PREFIX}/notes')
    app.register_blueprint(bp_users, url_prefix=f'{URL_PREFIX}/users')
