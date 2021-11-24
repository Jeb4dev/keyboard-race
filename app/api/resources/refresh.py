from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ..jwt import get_current_user, create_tokens_pair, set_refresh_token
from ..schemas import ErrorResponse
from ..schemas.auth import TokenResponse


class RefreshResource(Resource):
    """
    Resource for getting new access and refresh tokens
    """

    @jwt_required(refresh=True, locations=["cookies"])  # Require both tokens
    def post(self):
        user = get_current_user()
        if user:
            access_token, refresh_token = create_tokens_pair(user.username)
            set_refresh_token(refresh_token)
            return TokenResponse(access_token=access_token).dict()
        return ErrorResponse(error="Invalid identity").dict(), 401
