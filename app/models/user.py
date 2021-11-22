from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
from .db import db
from .statistics import Statistics


# Many to Many Races to Users


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(200))

    statistics = db.relationship('Statistics', backref='user', lazy=True, uselist=False)
    races = db.relationship(
        'Race',
        secondary='race_members',
        lazy='subquery',
        backref=db.backref('users', lazy=True)
    )

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def create(cls, username: str, password: str) -> "User":
        hashed_password = generate_password_hash(password, method='sha256')
        user = cls(
            username=username,
            password_hash=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        db.session.add(Statistics(user_id=user.id))
        db.session.commit()
        return user

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"
