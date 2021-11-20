from flask import Blueprint
from flask_restful import Api
from .resources import UserResource, LoginResource, LogoutResource, RefreshResource

router = Blueprint("api", __name__)
api = Api(router)

api.add_resource(UserResource, "/user/<int:user_id>")
api.add_resource(LoginResource, "/auth/login")
api.add_resource(LogoutResource, "/auth/logout")
api.add_resource(RefreshResource, "/auth/refresh")
