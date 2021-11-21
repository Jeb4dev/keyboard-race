from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.words import WordsEdit, WordsCreate


class WordsResource(Resource):
    def post(self, data: WordsCreate):
        """
        Create new race object
        """

    def get(self, user_id: int):
        """
        Get user profile info
        """
    @validate()
    def put(self, user_id: int, changes: WordsEdit):
        """
        Edit user profile
        """

    def delete(self, user_id: int):
        """
        Delete user profile
        """
