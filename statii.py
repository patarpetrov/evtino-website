from flask import Blueprint
from flask import render_template
from sqlalchemy.orm import sessionmaker
from app import engine, Post, Products

statii = Blueprint('statii', __name__, template_folder= 'templates', static_folder='static')

@statii.route('/')
def index():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()

    statii = sessiondb.query(Post).all()
    sessiondb.close()
    return render_template("allstatii.html", statii=statii)