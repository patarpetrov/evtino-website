from flask import Blueprint
from flask import render_template
from sqlalchemy.orm import sessionmaker
from app import engine, Post, Products, Productstore, Productstorespec

products = Blueprint('products', __name__, template_folder= 'templates', static_folder='static')

@products.route('/')
def index():
    print("1")
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    smartphones = sessiondb.query(Productstore).filter_by(category = "smartphone").all()

    sessiondb.close()
    
    return render_template("productsall.html", smartphones = smartphones)

@products.route('/<id>')
def product(id):
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    product = sessiondb.query(Productstore).filter_by(id = id).first()
    specification = sessiondb.query(Productstorespec).filter_by(main = id).first()
    return render_template("product.html", product = product, specification = specification)