from flask_restful import Resource
from flask_pydantic import validate

from app.models import User
from ..jwt import create_tokens_pair, set_refresh_token
from ..schemas import ErrorResponse
from ..schemas.auth import UserLogin, TokenResponse


class LoginResource(Resource):
    """
    Resource for login in users in app and giving them tokens
    """

    @validate()
    def post(self, data: UserLogin):
        user = User.query.filter_by(username=data.username).first()
        if user and user.check_password(data.password):
            access_token, refresh_token = create_tokens_pair(user.username)
            set_refresh_token(refresh_token)

            return TokenResponse(access_token=access_token)
        return ErrorResponse(error="Invalid credentials").dict(), 400
