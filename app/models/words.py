from sqlalchemy_serializer import SerializerMixin
from .db import db


class Words(db.Model, SerializerMixin):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.Text, nullable=False)
    words_title = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Words(id={self.id}, title={self.words_title})"
