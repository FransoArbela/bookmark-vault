from flask import session


def require_login():
    """Check if user is logged in and return user_id, or None if not logged in."""
    user_id = session.get("user_id")
    return user_id
