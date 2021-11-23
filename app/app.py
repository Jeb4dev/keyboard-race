from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO

from .settings import get_settings
from .models import db
from .api.api import router

app = Flask(__name__)

settings = get_settings()
app.config.from_object(settings)

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
jwt = JWTManager(app)
socketio = SocketIO(app)

app.register_blueprint(router, url_prefix="/api")
