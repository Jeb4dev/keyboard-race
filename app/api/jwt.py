from typing import Optional
from flask import after_this_request
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token, set_refresh_cookies

from app.models import User


def get_current_user(identity: Optional[str] = None):
    username = identity or get_jwt_identity()
    return User.query.filter_by(username=username).first() if username else None


def create_tokens_pair(identity: str):
    access_token = create_access_token(identity)
    refresh_token = create_refresh_token(identity)
    return access_token, refresh_token


def set_refresh_token(refresh_token: str):
    @after_this_request
    def set_refresh_token_in_cookies(response):
        # setting refresh token in cookie
        set_refresh_cookies(response, refresh_token)
        return response

    return set_refresh_token_in_cookies
