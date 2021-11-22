from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.words import WordsEdit, WordsCreate
from app.models import Words, db


class WordsResource(Resource):
    def get(self, words_id: int):
        """
        Get user profile info
        """
        word_list = Words.query.filter_by(id=words_id).first()
        return word_list

    @validate()
    def post(self, body: WordsCreate):
        """
        Create new words object
        """

        # Try get wordlist by words_title, if wordlist already exist raise ValueError
        word_list = Words.query.filter_by(words_title=body.words_title).first()
        if word_list:
            raise ValueError(f"Wordlist ({body.words_title}) already exist in database.")
        # Create new user object by calling create function from User class
        word_list.create(words_title=body.words_title, words=body.words)

    @validate()
    def put(self, words_id: int, body: WordsEdit):
        """
        Edit user profile
        """
        # Get username, password from changes and handle them
        words_object = Words.query.filter_by(id=words_id).first()
        if body.words_title:
            words_object.words_title = body.words_title
        if body.words:
            words_object.words = body.words
        db.session.commit()
