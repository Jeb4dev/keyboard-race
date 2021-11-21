from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.statistics import StatisticsDelete, StatisticsGet, StatisticsEdit
from app.models import User, Statistics
from app.models import db


class StatisticsResource(Resource):
    @staticmethod
    @validate()
    def post(user_id: int):
        """
        Create new static object
        """
        # Create statistics object for user
        user = User.query.filter_by(id=user_id).first()
        # Everything but id will be 0, as it is default
        new_statistics_object = Statistics()

        user.statistics.add(new_statistics_object)

        # Commit changes
        db.session.commit()

    @staticmethod
    def get(user_id: int, data: StatisticsGet):
        """
        Get statistics info
        """
        user = User.query.filter_by(id=user_id).first()
        # check if user has statistics object with that id
        if user.statistics.id == data.id:
            statistics = Statistics.query.filter_by(id=data.id).first()
            return statistics
        else:
            print(f"User ({user_id}) tried to get Statistics, but user has not statistics with id {data.id}")

    @staticmethod
    @validate()
    def put(user_id: int, data: StatisticsEdit):
        """
        Edit statistics info
        """
        user = User.query.filter_by(id=user_id).first()
        # check if user has static object with that id
        if user.statistics.id == data.id:
            statistics = Statistics.query.filter_by(id=data.id).first()
            if data.best_wpm:
                statistics.best_wpm = data.best_wpm
            if data.best_accuracy:
                statistics.best_accuracy = data.best_accuracy
            if data.total_races:
                statistics.total_races = data.total_races
            if data.total_wins:
                statistics.total_wins = data.total_wins
            if data.average_wpm:
                statistics.average_wpm = data.average_wpm
            if data.average_epm:
                statistics.average_epm = data.average_epm
            if data.average_accuracy:
                statistics.average_accurasy = data.average_accuracy
            if data.average_time:
                statistics.average_time = data.average_time
            db.session.commit()
        else:
            print(f"User ({user_id}) tried to edit statistics, but user has not statistics with id {data.id}")

    @staticmethod
    def delete(user_id: int, data: StatisticsDelete):
        """
        Delete statistics
        """
        user = User.query.filter_by(id=user_id).first()

        # check if user has statistics object with that id
        if user.statistics.id == data.id:
            statistics = Statistics.query.filter_by(id=data.id).first()
            db.session.delete(statistics)
            db.session.commit()
        else:
            print(f"User ({user_id}) tried to delete statistics, but user has not statistics with id {data.id}")
