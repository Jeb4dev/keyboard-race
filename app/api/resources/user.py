from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.user import UserEdit, UserCreate
from app.models import User
from app.models import db


class UserResource(Resource):
    def post(self, data: UserCreate):
        """
        Create new race object
        """
        # Try get user by username, if username already exist return
        user = User.query.filter_by(username=data.username).first()
        if user:
            raise ValueError(f"Username ({data.username}) already exist in database.")
        # Create new user object by calling create function from User class
        user.create(username=data.username, password=data.password)

    def get(self, user_id: int):
        """
        Get user profile info
        """
        user = User.query.filter_by(id=user_id).first()
        return user

    @validate()
    def put(self, user_id: int, changes: UserEdit):
        """
        Edit user profile
        """
        # Get username, password from changes and handle them
        if changes.password:
            user = User.query.filter_by(id=user_id).first()
            user.password_hash = user.generate_password_hash(changes.password)
        db.session.commit()

    def delete(self, user_id: int):
        """
        Delete user profile
        """
        user = User.query.filter_by(id=user_id).first()
        # does this also delete sub tables as user.
        db.session.delete(user)
        db.session.commit()
