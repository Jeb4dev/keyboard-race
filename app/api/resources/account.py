from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ..jwt import get_current_user


class AccountResource(Resource):
    @jwt_required()
    def get(self):
        user = get_current_user()
        return user.to_dict(rules=('-password', '-password_hash', '-races', '-statistics'))
