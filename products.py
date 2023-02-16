from flask import Blueprint, request
from flask import render_template

from sqlalchemy.orm import sessionmaker
from app import engine, ALLOWED_CATEGORIES, Post, Products, Productstore, Productstorespec

products = Blueprint('products', __name__, template_folder= 'templates', static_folder='static')

@products.route('/')
def index():
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
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
    
    #querying with filters   
    res2 = db
    res1 = []
    #print(tempdict['category'])
    if tempdict['category'] != []:
        for i in tempdict['category']:
            res2 = res2.filter_by(category  = i)
    
    if tempdict['ram']:
        #res1 = res2.all()
        for i in tempdict['ram']:
            #print(res2.filter_by(spec1 = i).all())
            #print("===================================")
            res1 += (res2.filter_by(spec1 = i).all())
    
    print(res1)
    if res1 == []:
        res1 = res2.all()
        return render_template("productsfiltered.html", products1 = res1, current_url=current_url)

    if res1 == [[]]:
        message = "No products found teu"
        print("no products found")
        sessiondb.close()
        return render_template("productsfiltered.html", products1 = res1, current_url=current_url)
    print(res2)
    sessiondb.close()
    return render_template("productsfiltered.html", products1 = res1, current_url=current_url)
    #return render_template("productsall.html", smartphones = smartphones, current_url = current_url)

@products.route('/product-<id>')
def product(id):
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
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
    sessiondb.close()
    return render_template("product.html", product = product, specification = specification, linkers = linkers, similar=similar)