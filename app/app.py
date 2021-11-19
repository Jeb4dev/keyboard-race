from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .settings import get_settings
from .models import db
from .api.api import router

app = Flask(__name__)

settings = get_settings()
app.config.from_object(settings)

db.init_app(app)

CORS(app)
JWTManager(app)

app.register_blueprint(router, url_prefix="/api")
