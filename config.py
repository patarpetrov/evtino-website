import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

UPLOAD_FOLDER_DIR = 'static/uploads/'

class Config:
    FLASK_DEBUG = "1"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    UPLOAD_FOLDER = UPLOAD_FOLDER_DIR
    SECRET_KEY = "malkiamesi"