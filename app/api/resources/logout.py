from flask import after_this_request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, unset_jwt_cookies


class LogoutResource(Resource):
    """
    Resource for logging out
    """

    @jwt_required()
    def post(self):
        @after_this_request
        def unset_cookies(response):
            unset_jwt_cookies(response)
            return response
