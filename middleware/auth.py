from flask import current_app, request
from functools import wraps
from typing import Callable
from werkzeug.security import check_password_hash


def login_required(f: Callable):
    @wraps(f)
    def wrapped(*args, **kwargs):
        auth = request.authorization
        unauthorized_response = ({
            'success': False,
            'error': 'Unauthorized'
        }, 401)

        if not auth:
            return unauthorized_response

        if auth.password is not None:
            # Client is attempting to authenticate as admin.
            # Check if username and password match.
            if not (auth.username == current_app.config['ADMIN_USER'] and \
                    check_password_hash(current_app.config['ADMIN_PASS'], auth.password)):
                return unauthorized_response

        return f(*args, **kwargs)

    return wrapped
