from sqlalchemy_serializer import SerializerMixin
from .db import db


class Statistics(db.Model, SerializerMixin):
    """
    Object that contains user statistics.
    """

    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True)
    best_wpm = db.Column(db.Integer, default=0)
    best_accuracy = db.Column(db.Integer, default=0)
    total_races = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)

    average_wpm = db.Column(db.Float, default=0)  # Average words per minute
    average_epm = db.Column(db.Float, default=0)  # Average errors per minute
    average_accuracy = db.Column(db.Float, default=0)  # Average Accuracy
    average_time = db.Column(db.Float, default=0)  # Average time the challenge took, in seconds

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Statistics(id={self.id})"

    #  How to get average
    #  https://stackoverflow.com/questions/44397844/sqlalchemy-get-average-of-greatest-n-per-group
