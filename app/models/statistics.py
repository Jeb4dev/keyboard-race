from .db import db


class Statistics(db.Model):
    __tabelname__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True)
    best_wpm = db.Column(db.Integer, default=0)
    total_races = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)

    average_wpm = db.Column(db.Integer, default=0)  # Average words per minute
    average_epm = db.Column(db.Integer, default=0)  # Average errors per minute
    average_accurasy = db.Column(db.Integer, default=0)  # Average Accuracy
    average_time = db.Column(db.Integer, default=0)  # Average time the challenge took, in seconds

    races = db.relationship('Race', backref='statistics')

    #  How to get average
    #  https://stackoverflow.com/questions/44397844/sqlalchemy-get-average-of-greatest-n-per-group
