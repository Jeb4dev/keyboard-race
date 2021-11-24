from flask_restful import Resource
from flask_pydantic import validate

from app.models import User
from ..jwt import create_tokens_pair, set_refresh_token
from ..schemas import ErrorResponse
from ..schemas.auth import UserLogin, AccountResponse


class LoginResource(Resource):
    """
    Resource for login in users in app and giving them tokens
    """

    @validate()
    def post(self, body: UserLogin):
        user = User.query.filter_by(username=body.username).first()
        if user and user.check_password(body.password):
            access_token, refresh_token = create_tokens_pair(user.username)
            set_refresh_token(refresh_token)

            return AccountResponse(access_token=access_token, user_id=user.id).dict()
        return ErrorResponse(error="Invalid credentials").dict(), 400
