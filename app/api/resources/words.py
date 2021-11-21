from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.words import WordsEdit, WordsCreate
from app.models import Words, db


class WordsResource(Resource):
    def post(self, data: WordsCreate):
        """
        Create new race object
        """

        # Try get wordlist by words_title, if wordlist already exist raise ValueError
        word_list = Words.query.filter_by(words_title=data.words_title).first()
        if word_list:
            raise ValueError(f"Wordlist ({data.words_title}) already exist in database.")
        # Create new user object by calling create function from User class
        word_list.create(words_title=data.words_title, words=data.words)

    def get(self, words_id: int):
        """
        Get user profile info
        """
        word_list = Words.query.filter_by(id=words_id).first()
        return word_list

    @validate()
    def put(self, words_id: int, changes: WordsEdit):
        """
        Edit user profile
        """
        # Get username, password from changes and handle them
        words_object = Words.query.filter_by(id=words_id).first()
        if changes.words_title:
            words_object.words_title = changes.words_title
        if changes.words:
            words_object.words = changes.words
        db.session.commit()

    def delete(self, words_id: int):
        """
        Delete user profile
        """
        words_object = Words.query.filter_by(id=words_id).first()
        # does this also delete sub tables as user.
        db.session.delete(words_object)
        db.session.commit()
