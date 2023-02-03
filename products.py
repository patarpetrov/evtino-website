from flask import Blueprint
from flask import render_template
from app import db, Post, Products, Productstore, Productstorespec

products = Blueprint('products', __name__, template_folder= 'templates', static_folder='static')

@products.route('/')
def index():
    smartphones = Productstore.query.filter_by(category = "smartphone").all()
    #all = Productstore.query.all()
    #all1 = db.session.query(Productstore).filer_by(Pro)all()
    print(all)
    for i in smartphones:
        print(str(i.category))
        #if i.category !='':
            #print(i.category)
    return render_template("productsall.html", smartphones = smartphones)