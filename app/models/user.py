from werkzeug.security import generate_password_hash, check_password_hash
from .db import db


class User(db.Model):
    __tabelname__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(200))

    statistics = db.relationship('Statistics', backref='user')

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username: str, password: str):
        hashed_password = generate_password_hash(password, method='sha256')
        user = cls(
            username=username,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
