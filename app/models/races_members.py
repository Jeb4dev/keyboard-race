from .db import db


class RaceMembers(db.Model):
    __tablename__ = 'race_members'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))
