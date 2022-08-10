from flask import request
from models.session import Session


def get_user_id() -> int | None:
    # Get session ID from cookie
    session_id = request.cookies.get('session_id')

    # Get session
    session = Session.query.filter_by(id=session_id).first()

    # Return user ID
    return session.user_id if session else None
