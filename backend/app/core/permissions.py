from fastapi import Depends

from app.core.dependencies import get_current_user


def require_user():
    """
    Returns the currently authenticated user.
    Can be extended later for role-based authorization.
    """
    return Depends(get_current_user)