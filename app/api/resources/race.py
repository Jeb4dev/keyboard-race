from flask_restful import Resource
from flask_pydantic import validate

from app.api.schemas.race import RaceCreate, RaceDelete, RaceGet, RaceEdit
from app.api.schemas.statistics import StatisticsEdit
from app.models import User, Race
from app.models import db
from app.api.resources import statistics


class RaceResource(Resource):
    def post(self, user_id: int, data: RaceCreate):
        """
        Create new race object
        """
        # Get ranking, total_participants, wpm, epm, accuracy, time from data
        # and update user.statistics.race with new object.
        user = User.query.filter_by(id=user_id).first()
        new_db_object = Race(ranking=data.ranking, total_participants=data.total_participants,
                             wpm=data.wpm, epm=data.wpm, accuracy=data.accuracy, time=data.time)

        user.statistics.races.append(new_db_object)

        # Commit changes
        db.session.commit()

        # Update statistics object with new averages etc.
        if data.wpm > user.statistics.best_wpm:
            best_wpm = data.wpm
        else:
            best_wpm = user.statistics.best_wpm
        total_races = user.statistics.total_races + 1

        if data.ranking == 1:
            total_wins = user.statistics.total_wins + 1
        else:
            total_wins = user.statistics.total_wins

        # if it is users first race average records are same than current race records
        if total_races == 1:
            average_wpm = data.wpm

            average_epm = data.epm

            average_accuracy = data.accuracy

            average_time = data.time

        # else recalculate average values
        else:
            average_wpm = (user.statistics.average_wpm * (total_races - 1) + data.wpm) / total_races

            average_epm = (user.statistics.average_epm * (total_races - 1) + data.epm) / total_races

            average_accuracy = (user.statistics.average_accurasy * (total_races - 1) + data.accuracy) / total_races

            average_time = (user.statistics.average_time * (total_races - 1) + data.time) / total_races

        data = StatisticsEdit(best_wpm=best_wpm, total_races=total_races, total_wins=total_wins, average_wpm=average_wpm,
                              average_epm=average_epm, average_accuracy=average_accuracy, average_time=average_time)

        statistics.StatisticsResource.put(user_id=user_id, data=data)

    def get(self, user_id: int, data: RaceGet):
        """
        Get race info
        """
        user = User.query.filter_by(id=user_id).first()
        # check if user has race object with that id
        if user.statistics.races.id == data.id:
            race = Race.query.filter_by(id=data.id).first()
            return race
        else:
            print(f"User ({user_id}) tried to get race, but user has not race with id {data.id}")

    def put(self, user_id: int, data: RaceEdit):
        """
        Edit race info
            'I don't think we need to edit race info...' - Jeb
        """
        user = User.query.filter_by(id=user_id).first()
        # check if user has race object with that id
        if user.statistics.races.id == data.id:
            race = Race.query.filter_by(id=data.id).first()
            if data.ranking:
                race.ranking = data.ranking
            if data.total_participants:
                race.total_participants = data.total_participants
            if data.wpm:
                race.wpm = data.wpm
            if data.epm:
                race.epm = data.epm
            if data.accuracy:
                race.accuracy = data.accuracy
            if data.time:
                race.time = data.time
            db.session.commit()
        else:
            print(f"User ({user_id}) tried to edit race, but user has not race with id {data.id}")

    def delete(self, user_id: int, data: RaceDelete):
        """
        Delete race
        """
        user = User.query.filter_by(id=user_id).first()

        # check if user has race object with that id
        if user.statistics.races.id == data.id:
            race = Race.query.filter_by(id=data.id).first()
            db.session.delete(race)
            db.session.commit()
        else:
            print(f"User ({user_id}) tried to delete race, but user has not race with id {data.id}")
