from datetime import datetime
from flask import current_app, request
from functools import wraps
from models.discord_oauth2 import DiscordOAuth2
from models.session import Session
from typing import Callable
from werkzeug.security import check_password_hash


UNAUTHORIZED = ({
    'success': False,
    'error': 'Unauthorized'
}, 401)


def login_required(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        session_id = request.cookies.get('session_id')

        if auth is not None:
            # Client is attempting to authenticate using the Authentiation header.
            if auth.password is not None:
                # Client is attempting to authenticate as admin.
                # Check if username and password match.
                if not (auth.username == current_app.config['ADMIN_USER'] and
                        check_password_hash(current_app.config['ADMIN_PASS'], auth.password)):
                    return UNAUTHORIZED
            else:
                # Client is attempting to authenticate using a method other than Basic.
                return UNAUTHORIZED
        else:
            # Client is not attempting to authenticate using the Authentication header.

            if not session_id:
                # Client did not provide either an authorization header or a session ID cookie.
                return UNAUTHORIZED

            # Check if session is in DB
            session = Session.query.filter_by(id=session_id).first()
            if session is None:
                return UNAUTHORIZED

            # Check if session is expired
            if session.expires_at < datetime.now():
                return UNAUTHORIZED

            # Check if Discord tokens are in DB
            discord_oauth2 = DiscordOAuth2.query.filter_by(session_id=session_id).first()
            if discord_oauth2 is None:
                return UNAUTHORIZED

            # Check if Discord tokens are expired
            if discord_oauth2.expires_at < datetime.now():
                return UNAUTHORIZED

        return f(*args, **kwargs)

    return wrapped


def admin_only(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return UNAUTHORIZED

        if auth.password is not None:
            # Client is attempting to authenticate as admin.
            # Check if username and password match.
            if not (auth.username == current_app.config['ADMIN_USER'] and
                    check_password_hash(current_app.config['ADMIN_PASS'], auth.password)):
                return UNAUTHORIZED
        else:
            return UNAUTHORIZED

        return f(*args, **kwargs)

    return wrapped
