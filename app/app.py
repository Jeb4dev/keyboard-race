from flask import Flask
from .settings import get_settings
from .models import db

settings = get_settings()

app = Flask(__name__)

app.config.from_object(settings)

db.init_app(app)
