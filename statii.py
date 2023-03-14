from flask import Blueprint
from flask import render_template
from sqlalchemy.orm import sessionmaker
from app import engine, Post, Products
from functions import *

statii = Blueprint('statii', __name__, template_folder= 'templates', static_folder='static')

@statii.route('/')
def index():
    sessiondb = sessionMake(engine)

    statii = sessiondb.query(Post).all()
    sessiondb.close()
    return render_template("allstatii.html", statii=statii)


@statii.route('/<slug>')
def statiaLoad(slug):
    sessiondb = sessionMake(engine)

    statia = sessiondb.query(Post).filter_by(slug = slug).first()
    products = sessiondb.query(Products).filter_by(pageused = statia).all()
    
    sessiondb.close()
    return render_template("statia.html", statia = statia, products = products)