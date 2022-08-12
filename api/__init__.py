from flask import request
from models.session import Session


def get_user_id() -> int | None:
    # Get session ID from auth header
    auth_method, session_id = request.headers.get('Authorization', '').split(' ')
    if auth_method != 'Bearer' or not session_id:
        return None

    # Get session
    session = Session.query.filter_by(id=session_id).first()

    # Return user ID
    return session.user_id if session else None
