from flask_restful import Resource

from app.models import User


class StatisticsResource(Resource):
    def get(self, user_id: int):
        """
        Get statistics info
        """
        user = User.query.filter_by(id=user_id).first()
        if user:
            return {
                "statistics": user.statistics.to_dict(rules=('-id', '-user_id', '-user')),
                "races": [race.to_dict() for race in user.races]
            }
        return "", 404
