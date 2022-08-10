from datetime import datetime
from flask import current_app, request
from functools import wraps
from models.discord_oauth2 import DiscordOAuth2
from models.session import Session
from typing import Callable, TYPE_CHECKING
from werkzeug.security import check_password_hash
if TYPE_CHECKING:
    from werkzeug.datastructures import Authorization


def unauthorized(err: str | Exception):
    return ({
        'success': False,
        'error': 'Unauthorized',
        'reason': str(err)
    }, 401)


def check_basic_auth(auth: 'Authorization'):
    if auth is None:
        raise RuntimeError('No credentials provided')

    # Client is attempting to authenticate using the Authentication header.
    if auth.password is not None:
        # Client is attempting to authenticate as admin.
        # Check if username and password match.
        if not (auth.username == current_app.config['ADMIN_USER'] and
                check_password_hash(current_app.config['ADMIN_PASS'], auth.password)):
            raise ValueError('Unrecognized credentials')
    else:
        # Client is attempting to authenticate using a method other than Basic.
        raise ValueError('Unrecognized auth method')


def check_cookie(session_id: str | None):
    if not session_id:
        # Client did not provide either an authorization header or a session ID cookie.
        raise RuntimeError('No credentials provided')

    # Check if session is in DB
    session = Session.query.filter_by(id=session_id).first()
    if session is None:
        raise ValueError('Invalid session ID')

    # Check if session is expired
    if session.expires_at < datetime.now():
        raise ValueError('Session expired')

    # Check if Discord tokens are in DB
    discord_oauth2 = DiscordOAuth2.query.filter_by(session_id=session_id).first()
    if discord_oauth2 is None:
        raise ValueError('Discord tokens not found')

    # Check if Discord tokens are expired
    if discord_oauth2.expires_at < datetime.now():
        raise ValueError('Discord tokens expired')


def login_required(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        session_id = request.cookies.get('session_id')

        if auth is not None:
            try:
                check_basic_auth(auth)
            except RuntimeError:
                pass
            except ValueError as e:
                return unauthorized(e)

        if session_id is not None:
            # Client is not attempting to authenticate using the Authentication header.
            try:
                check_cookie(session_id)
            except Exception as e:
                return unauthorized(e)

        return f(*args, **kwargs)

    return wrapped


def admin_only(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization

        try:
            check_basic_auth(auth)
        except Exception as e:
            return unauthorized(e)

        return f(*args, **kwargs)

    return wrapped


def user_only(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        session_id = request.cookies.get('session_id')

        try:
            check_cookie(session_id)
        except Exception as e:
            return unauthorized(e)

        return f(*args, **kwargs)

    return wrapped
