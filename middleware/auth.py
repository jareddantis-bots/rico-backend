from flask import current_app, request
from functools import wraps
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

        if not auth:
            return UNAUTHORIZED

        if auth.password is not None:
            # Client is attempting to authenticate as admin.
            # Check if username and password match.
            if not (auth.username == current_app.config['ADMIN_USER'] and
                    check_password_hash(current_app.config['ADMIN_PASS'], auth.password)):
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
