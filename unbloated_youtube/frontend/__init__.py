from flask import Flask
from api import settings
import os


settings_file_path = os.path.join(os.path.dirname(__file__), "settings.json")
app = Flask(__name__)
SETTINGS_OBJ = settings.Settings(path=settings_file_path)

