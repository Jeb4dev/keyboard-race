from flask_restful import Resource
from flask_pydantic import validate
from flask_jwt_extended import jwt_required

from app.api.schemas import ErrorResponse
from app.api.schemas.user import UserEdit
from app.models import User, db
from app.api.jwt import get_current_user


class UserResource(Resource):
    def get(self, user_id: int):
        """
        Get user profile info
        """
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.to_dict(rules=('-password', '-password_hash', '-races', '-statistics'))
        return ErrorResponse(error="User not found").dict(), 404

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

    @jwt_required()
    def delete(self, user_id: int):
        """
        Delete user profile
        """
        user = get_current_user()
        delete_user = User.query.filter_by(id=user_id).first()
        if user and delete_user and user == delete_user:
            db.session.delete(user)
            db.session.commit()
            db.session.delete(delete_user.statistics)
