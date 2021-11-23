from flask import Blueprint
from flask_restful import Api
from .resources import UserResource, LoginResource, LogoutResource, RefreshResource, RegisterResource, \
    StatisticsResource, AccountResource

router = Blueprint("api", __name__)
api = Api(router)

api.add_resource(UserResource, "/user/<int:user_id>")
api.add_resource(LoginResource, "/auth/login")
api.add_resource(LogoutResource, "/auth/logout")
api.add_resource(RefreshResource, "/auth/refresh")
api.add_resource(RegisterResource, "/auth/register")
api.add_resource(StatisticsResource, "/statistics/<int:user_id>")
api.add_resource(AccountResource, "/user/account")
