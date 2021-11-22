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

    def __repr__(self):
        return ("Race("
                f"id={self.id}, "
                f"date(exact time when )={self.date}, "
                f"ranking(how did player rank)={self.ranking}, "
                f"total_participants(total amount of player)={self.total_participants}, "
                f"wpm(words per minute)={self.wpm}, "
                f"epm(errors per minute)={self.epm}, "
                f"accuracy(in per cents 0-100)={self.accuracy}, "
                f"time(how long did the challenge take)={self.time}, "
                ")"
                )
