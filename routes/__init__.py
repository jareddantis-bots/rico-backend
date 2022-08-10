from typing import TYPE_CHECKING
from .auth import bp_auth
from .discord import bp_discord
from .excluded_threads import bp_excluded_threads
from .guilds import bp_guilds
from .health import bp_health
from .notes import bp_notes
from .users import bp_users
if TYPE_CHECKING:
    from flask import Flask


def install_routes(app: 'Flask'):
    url_prefix = app.config['API_URL_PREFIX']

    app.register_blueprint(bp_health)
    app.register_blueprint(bp_auth, url_prefix=url_prefix)
    app.register_blueprint(bp_discord, url_prefix=url_prefix)
    app.register_blueprint(bp_excluded_threads, url_prefix=url_prefix)
    app.register_blueprint(bp_guilds, url_prefix=url_prefix)
    app.register_blueprint(bp_notes, url_prefix=url_prefix)
    app.register_blueprint(bp_users, url_prefix=url_prefix)
