from flask import Blueprint, request
from flask import render_template
from functions import *

from sqlalchemy.orm import sessionmaker
from app import engine, ALLOWED_CATEGORIES, Post, Products, Productstore, Productstorespec

products = Blueprint('products', __name__, template_folder= 'templates', static_folder='static')

@products.route('/')
def index():
    #Session = sessionmaker(bind=engine)
    #sessiondb = Session()
    sessiondb = sessionMake(engine)
    db = sessiondb.query(Productstore).join(Productstorespec, Productstorespec.main == Productstore.id, isouter=True)
    smartphones = db.filter_by(category = "smartphone").all()

    
    current_url = request.full_path
    splited = current_url.split('?')
    # print(splited[0])
    # print(splited[1])
    param = splited[1].split('&')
    #new_url = splited[0]
    tempdict = {}
    
    tempdict.setdefault('category', [])
    tempdict.setdefault('ram', [])
    #reading every parametar from url
    for i in range(len(param)):
        argument, value = '', ''
        if param[i] != '':
            splitedpara = param[i].split("=")
            argument = splitedpara[0]
            if splitedpara[1]:
                value = splitedpara[1]

        if value == "none":
            pass
        else:
            tempdict.setdefault(argument, [])
            tempdict[argument].append(value)
    

    res2 = db
    res1 = []
    lamp = 0

    if tempdict['category'] != []:
        lamp = 1
        for i in tempdict['category']:
            res2 = res2.filter_by(category  = i)
    
    if tempdict['ram']:
        lamp = 2
        for i in tempdict['ram']:
            res1 += (res2.filter_by(spec4 = i).all())

    print(res1)
    if res1 == [] and lamp == 1:
        if lamp:
            print("2")
            products1 = res2.all()
            return render_template("productsfiltered.html", products1 = products1, current_url = current_url)
        else:
            print("1")
            smartphones = res2.filter_by(category = "smartphone")
            tvs = res2.filter_by(category = "tv")
            sessiondb.close()
            return render_template("productsall.html", smartphones = smartphones, tvs = tvs, current_url=current_url)

    smartphones = res2.filter_by(category = "smartphone")
    tvs = res2.filter_by(category = "tv")
    sessiondb.close()
    return render_template("productsall.html", smartphones = smartphones, tvs = tvs, current_url=current_url)
    #sessiondb.close()
    #if res1 == []
    #return render_template("productsfiltered.html", products1 = res1, current_url = current_url)

@products.route('/product-<id>')
def product(id):
    #Session = sessionmaker(bind=engine)
    #sessiondb = Session()
    sessiondb = sessionMake(engine)
    linkers = []
    product = sessiondb.query(Productstore).filter_by(id = id).first()
    specification = sessiondb.query(Productstorespec).filter_by(main = id).first()
    print(type(specification.linker1))
    linkers.append(sessiondb.query(Productstore).filter_by(id = specification.linker1).first())
    linkers.append(sessiondb.query(Productstore).filter_by(id = specification.linker2).first())
    linkers.append(sessiondb.query(Productstore).filter_by(id = specification.linker3).first())
    linkers.append(sessiondb.query(Productstore).filter_by(id = specification.linker4).first())
    linkers.append(sessiondb.query(Productstore).filter_by(id = specification.linker5).first())
    print(linkers)
    similar = sessiondb.query(Productstore).join(Productstorespec, Productstorespec.main == Productstore.id, isouter=True).filter_by(category = specification.category).limit(5).all()
    print(similar)
    print(specification)
    sessiondb.close()
    return render_template("product.html", product = product, specification = specification, linkers = linkers, similar=similar)