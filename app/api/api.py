from flask import Blueprint
from flask_restful import Api

router = Blueprint("api", __name__)
api = Api(router)
