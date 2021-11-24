from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas import ErrorResponse
from app.api.schemas.user import UserCreate
from app.api.schemas.auth import AccountResponse
from app.models import User
from app.api.jwt import create_tokens_pair, set_refresh_token


class RegisterResource(Resource):
    @validate()
    def post(self, body: UserCreate):
        """
        Create new User object
        """
        # Try get user by username, if username already exist return
        if User.query.filter_by(username=body.username).first() is not None:
            return ErrorResponse(error=f"Username ({body.username}) already exist in database.").dict(), 400

        # Create new user object by calling create function from User class
        user = User.create(username=body.username, password=body.password)
        access_token, refresh_token = create_tokens_pair(user.username)
        set_refresh_token(refresh_token)
        return AccountResponse(access_token=access_token, user_id=user.id).dict(), 201
