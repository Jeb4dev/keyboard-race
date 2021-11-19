from flask import Blueprint
from flask_restful import Api
from .resources import UserResource

router = Blueprint("api", __name__)
api = Api(router)

api.add_resource(UserResource, "/user/<int:user_id>")
