from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from .db import db


class Race(db.Model, SerializerMixin):
    """
    This object has statistics of particular race of user
    """

    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    ranking = db.Column(db.Integer, nullable=False)
    total_participants = db.Column(db.Integer, default=0)

    wpm = db.Column(db.Integer, default=0)  # Words per minute
    epm = db.Column(db.Integer, default=0)  # Errors per minute
    accuracy = db.Column(db.Integer, default=0)  # Accuracy
    time = db.Column(db.Integer, default=0)  # Time that user used in challenge, in seconds
    errors = db.Column(db.String(1000), default="")  # JSON object of count of misstyped characters.
    # TODO: Check if adding errors column is done correctly, should it be referred elsewhere?

    def __repr__(self):
        return f"Race(id={self.id})"
