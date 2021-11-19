from .db import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# This file contains modules of objects saved in database
# __init__ and __repr__ and some other functions are not yet fully ready


class User(db.Model):
    __tabelname__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(200))

    statistics = db.relationship('Statistics', backref='user')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password, method='sha256')

    def __repr__(self):
        # How to add
        return f"id={self.id}, username={self.username}, password_hash={self.password_hash}"


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

    races = db.relationship('Races', backref='statistics')

    #  How to get average
    #  https://stackoverflow.com/questions/44397844/sqlalchemy-get-average-of-greatest-n-per-group


class Races(db.Model):
    __tabelname__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    ranking = db.Column(db.Integer)
    total_participants = db.Column(db.Integer)

    wpm = db.Column(db.Integer)  # Words per minute
    epm = db.Column(db.Integer)  # Errors per minute
    accuracy = db.Column(db.Integer)  # Accuracy
    time = db.Column(db.Integer)  # Time that user used in challenge, in seconds

    def __init__(self, ranking, participants=0, wpm=0, epm=0, accuracy=0, time=0):
        self.ranking = int(ranking)
        self.total_participants = int(participants)
        self.wpm = int(wpm)
        self.epm = int(epm)
        self.accuracy = int(accuracy)
        self.time = int(time)

    def __repr__(self):
        return (f"This object has statistics of particular race of user"  # Add users name or id
                f"id={self.id}, "
                f"date(exact time when )={self.date}, "
                f"ranking(how did player rank)={self.ranking}, "
                f"total_participants(total amount of player)={self.total_participants}, "
                f"wpm(words per minute)={self.wpm}, "
                f"epm(errors per minute)={self.epm}, "
                f"accuracy(in per cents 0-100)={self.accuracy}, "
                f"time(how long did the challenge take)={self.time}, ")


class Words(db.Model):
    __tabelname__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    words = db.Column(db.String(1000), nullable=False)
