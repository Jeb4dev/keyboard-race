from flask import Flask
from . import settings

settings = settings.get_settings()

app = Flask(__name__)
