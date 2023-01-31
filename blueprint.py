from flask import Blueprint
from flask import render_template
from app import db, Post, Products

statii = Blueprint('statii', __name__, template_folder= 'templates', static_folder='static')

@statii.route('/')
def index():
    res = Post.query.first()
    
    return render_template("statii.html", statia = res)