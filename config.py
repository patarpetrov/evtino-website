import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

UPLOAD_FOLDER_DIR = 'static/uploads/'

class Config:
    FLASK_DEBUG = "1"
    SQLALCHEMY_DATABASE_URI = 'postgresql://evtino_user:7Gn99jhwihLA8EVcNIZCdI1fZhIt7IqG@dpg-cfcis3en6mpierpgf3h0-a.frankfurt-postgres.render.com/evtino'
    TEMPLATES_AUTO_RELOAD = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    UPLOAD_FOLDER = UPLOAD_FOLDER_DIR
    SECRET_KEY = "malkiamesi"