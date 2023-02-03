from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import ForeignKey
from bs4 import BeautifulSoup
import requests
import boto3
import uuid


from config import Config
#from statii.blueprint import statii

import json
import urllib.request
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secret key"
print(os.getenv('AWS_SECRET_ACCESS_KEY'))
Session(app)

db = SQLAlchemy(app)
from models import *
#admin.add_view(ModelView(Post, db.session))
#admin.add_view(ModelView(Products, db.session))

with app.app_context():
    #Productstore.__table__.drop(db.engine)
    db.create_all()

BUCKET_NAME = "evtino"
#s3 = boto3.client("s3", aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))
s3 = boto3.resource("s3")

ALLOWED_CATEGORIES = set(['smartphone', 'laptop', ''])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    #filename = secure_filename(file.filename)
    new_filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
    s3.Bucket(BUCKET_NAME).upload_fileobj(file, new_filename)
    return new_filename

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("usr") is None:
            return redirect("/admin-login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        with open("./static/top5.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(type(data))
        return render_template("homepage1.html", dict1 = data)

    #if request.method =="POST":
        #email = request.form.get("buletina")
        #with open("./static/emails.csv", "r", encoding="utf-8") as f:
            #pass
'''
@app.route("/statii")
def statii():
    res = Post.query.first()
    print(res)
    return render_template("statii.html")'''



@app.route("/admin-login", methods=["GET", "POST"])
def d():
    if request.method == "GET":
        return render_template("d.html")
    if request.method == "POST":
        with open("./static/d.json", "r") as f:
            data = json.load(f)
            user = request.form.get("user")
            pas = request.form.get("pas")
            if not check_password_hash(data['usr'], user) or not check_password_hash(data['psw'], pas):
                print("wrong pass")
                return render_template("d.html")
            else: 
                session['usr'] = 0
                print("d.")
                return redirect("/admin")


@app.route("/admin", methods=["GET", "POST"])
@login_required
def din():
    if request.method == "GET":
        print("da")
        return render_template("din.html")
        

@app.route("/adminnapishi", methods = ["GET", "POST"])
@login_required
def napishi():
    if request.method == "GET":
        return render_template("din-napishi.html")
    if request.method == "POST":
        files1 =[]
        file = request.files['file']
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        file4 = request.files['file4']
        files = [file, file1, file2, file3, file4]

        title = request.form.get("title")
        category = request.form.get("category")
        slug = request.form.get("slug")

        specList = [request.form.get("spec1"), request.form.get("spec2"), request.form.get("spec3"), request.form.get("spec4"), request.form.get("spec5"), request.form.get("spec6")]
        product_name=[request.form.get("productname"), request.form.get("productname1"), request.form.get("productname2"), request.form.get("productname3"), request.form.get("productname4")]
        content = [request.form.get("content"), request.form.get("content1"), request.form.get("content2"), request.form.get("content3"), request.form.get("content4")]
        spec1answ = [request.form.get("1spec1answ"), request.form.get("1spec2answ"), request.form.get("1spec3answ"), request.form.get("1spec4answ"), request.form.get("1spec5answ"), request.form.get("1spec6answ")]
        spec2answ = [request.form.get("2spec1answ"), request.form.get("2spec2answ"), request.form.get("2spec3answ"), request.form.get("2spec4answ"), request.form.get("2spec5answ"), request.form.get("2spec6answ")]
        spec3answ = [request.form.get("3spec1answ"), request.form.get("3spec2answ"), request.form.get("3spec3answ"), request.form.get("3spec4answ"), request.form.get("3spec5answ"), request.form.get("3spec6answ")]
        spec4answ = [request.form.get("4spec1answ"), request.form.get("4spec2answ"), request.form.get("4spec3answ"), request.form.get("4spec4answ"), request.form.get("4spec5answ"), request.form.get("4spec6answ")]
        spec5answ = [request.form.get("5spec1answ"), request.form.get("5spec2answ"), request.form.get("5spec3answ"), request.form.get("5spec4answ"), request.form.get("5spec5answ"), request.form.get("5spec6answ")]

        for file in files:
            new_filename = ''
            if file.filename == '':
                message = 'No image selected for uploading'
                pass
            #render_template("din-napishi.html", message = message)
        
            if file and allowed_file(file.filename):
                new_filename =  save_file(file)
                files1.append(new_filename)
            else:
                print(file)
                message = 'Allowed image types are - png, jpg, jpeg, gif'
                #return render_template("din-napishi.html", message = message)
                
        post_new = Post(slug = slug, title = title, category = category, spec1 = specList[0], spec2 = specList[1], spec3 = specList[2], spec4 = specList[3], spec5 = specList[4], spec6 = specList[5])
        db.session.add(post_new)
        db.session.commit()
    
        obj = db.session.query(Post).order_by(Post.id.desc()).first()
        
        products = Products(store = "emag", pageused = obj, productname = product_name[0], imagepath = files1[0], content = content[0], spec1answ = spec1answ[0], spec2answ = spec1answ[1], spec3answ = spec1answ[2], spec4answ = spec1answ[3], spec5answ = spec1answ[4], spec6answ = spec1answ[5])
        products1 = Products(store = "emag", pageused = obj, productname = product_name[1], imagepath = files1[1], content = content[1], spec1answ = spec2answ[0], spec2answ = spec2answ[1], spec3answ = spec2answ[2], spec4answ = spec2answ[3], spec5answ = spec2answ[4], spec6answ = spec2answ[5])
        products2 = Products(store = "emag", pageused = obj, productname = product_name[2], imagepath = files1[2], content = content[2], spec1answ = spec3answ[0], spec2answ = spec3answ[1], spec3answ = spec3answ[2], spec4answ = spec3answ[3], spec5answ = spec3answ[4], spec6answ = spec3answ[5])
        products3 = Products(store = "emag", pageused = obj, productname = product_name[3], imagepath = files1[3], content = content[3], spec1answ = spec4answ[0], spec2answ = spec4answ[1], spec3answ = spec4answ[2], spec4answ = spec4answ[3], spec5answ = spec4answ[4], spec6answ = spec4answ[5])
        products4 = Products(store = "emag", pageused = obj, productname = product_name[4], imagepath = files1[4], content = content[4], spec1answ = spec5answ[0], spec2answ = spec5answ[1], spec3answ = spec5answ[2], spec4answ = spec5answ[3], spec5answ = spec5answ[4], spec6answ = spec5answ[5])
        products_list = [products, products1, products2, products3, products4]
        db.session.add(products)
        db.session.add(products1)
        db.session.add(products2)
        db.session.add(products3)
        db.session.add(products4)
        db.session.commit()
        return render_template("statii.html", statia = post_new, productslist = products_list)

@app.route("/adminproduct", methods = ["GET", "POST"])
@login_required
def product():
    if request.method == "GET":
        return render_template("adminproduct.html")
    if request.method == "POST":
        link = request.form.get("link")
        storename = str(request.form.get("storename"))
        header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
}
        html_text = requests.get(link ,headers=header).text
        soup = BeautifulSoup(html_text, 'lxml')
        existing = []
        print(storename)
        if storename == "emag":
            products = soup.find_all('div', class_ = "card-item card-standard js-product-data")
            
            for product in products:
                productname1 = product.find('a', class_ = "card-v2-title semibold mrg-btm-xxs js-product-url").text.replace("  ", "")
                image1 = product.find('img')["src"]
                price = int(product.find('p', class_ = "product-new-price").text.replace(" лв", "").replace(".", "").replace(",", "").replace(".", "").replace("от ", ""))
                st1 = f'{(price%100):02}'

                new_product = Productstore(category = '', store = "emag", productname = productname1, imagesrc = image1, lev = price//100, st = st1)
                exist = Productstore.query.filter_by(productname = new_product.productname).first()
                print(new_product.productname)
                nochange = 0
                if exist:
                    if exist.lev == new_product.lev:
                        nochange += 1 
                    else:
                        razlika = int(exist.lev) - int(new_product.lev)
                        if razlika > 10:
                            exist.levsale = new_product.lev
                            exist.stsale = new_product.st
                        else:
                            exist.lev = new_product.lev
                            exist.st = new_product.st
                            exist.levsale = None
                            exist.stsale = None
                        db.session.commit()

                else:
                    print("2")
                    db.session.add(new_product)
                    db.session.commit()


        if storename == "technopolis":
            print("1")
            products = soup.find_all('div', class_ = "product-box js-product__box")
            print(products)
            for product in products:
                productname1 = product.find('a', class_ = "product-box__title-link").text.replace("  ", "")
                price = int(product.find('span', class_ = "product-box__price-value").text.replace(" лв", "").replace(".", "").replace(",", "").replace(".", "").replace(" ", ""))
                st1 = str(product.find('sup').text)

                new_product = Productstore(category = '', store = "technopolis", productname = productname1, lev = price, st = st1)
                exist = Productstore.query.filter_by(productname = new_product.productname).first()
                nochange = 0
                if exist:
                    if exist.lev == new_product.lev:
                        nochange += 1 
                    else:
                        razlika = int(exist.lev) - int(new_product.lev)
                        if razlika > 10:
                            exist.levsale = new_product.lev
                            exist.stsale = new_product.st
                        else:
                            exist.lev = new_product.lev
                            exist.st = new_product.st
                            exist.levsale = None
                            exist.stsale = None
                        db.session.commit()

                else:
                    print("2")
                    db.session.add(new_product)
                    db.session.commit()

        #print(existing)
        #print(len(existing))
        all = Productstore.query.all()
        return redirect("/adminnspecpro")
        #return render_template("products.html", products1 = all, length = len(existing))


@app.route("/adminnspecpro", methods = ["GET", "POST"])
@login_required
def prodspec():
    if request.method == "GET": 
        res = Productstore.query.all()
        return render_template("productspec.html", products1 = res)

@app.route("/adminnspecpro<id>", methods = ["GET", "POST"])
@login_required
def prodspec1(id):
    if request.method == "GET":
        product = Productstore.query.filter_by(id = id).first()
        return render_template("admaddprodspec.html", product = product)

    if request.method == "POST":
        new = Productstorespec()
        files1 = []
        res = db.session.query(Productstore).filter_by(id = id).first()
        res1 = Productstore.query.filter_by(id = id).first()
        files = [request.files['file1'], request.files['file2'], request.files['file3'], request.files['file4'], request.files['file5'], request.files['file6'], request.files['file7'], request.files['mainimage']]
        for file in files:
            if file.filename != '' and allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                new_filename = save_file(file)
                emag_filename = f"https://evtino.s3.eu-central-1.amazonaws.com/{new_filename}"
                files1.append(emag_filename)
            else:
                files1.append('')

        if request.form.get('category') != '' : res1.category = request.form.get('category')
        if files1[7] != '': res1.imagesrc = files1[7]
        db.session.commit()
        if files1[0] != '':
            new.imagepath1 = files1[0]
        if files1[1] != '':
            new.imagepath2 = files1[1]
        if files1[2] != '':
            new.imagepath3 = files1[2]
        if files1[0] != '':
            new.imagepath4 = files1[3]
        if files1[0] != '':
            new.imagepath5 = files1[4]
        if files1[0] != '':
            new.imagepath6 = files1[5]
        if files1[0] != '':
            new.imagepath7 = files1[6]
        if request.form.get('link1') != '':
            new.link1 = request.form.get("link1")
        if request.form.get('link2') != '':
            new.link2 = request.form.get("link2")
        if request.form.get('link3') != '':
            new.link3 = request.form.get("link3")
        if request.form.get('link4') != '':
            new.link4 = request.form.get("link4")
        if request.form.get('link5') != '':
            new.link5 = request.form.get("link5")

        if request.form.get("spec1") != '': new.spec1 = request.form.get("spec1")
        if request.form.get("spec2") != '': new.spec2 = request.form.get("spec2")
        if request.form.get("spec3") != '': new.spec3 = request.form.get("spec3")
        if request.form.get("spec4") != '': new.spec4 = request.form.get("spec4")
        if request.form.get("spec5") != '': new.spec5 = request.form.get("spec5")
        if request.form.get("spec6") != '': new.spec6 = request.form.get("spec6")
        if request.form.get("spec7") != '': new.spec7 = request.form.get("spec7")
        if request.form.get("spec8") != '': new.spec8 = request.form.get("spec8")
        if request.form.get("spec9") != '': new.spec9 = request.form.get("spec9")
        if request.form.get("spec10") != '': new.spec10 = request.form.get("spec10")
        if request.form.get("spec11") != '': new.spec11 = request.form.get("spec11")
        if request.form.get("spec12") != '': new.spec12 = request.form.get("spec12")
        if request.form.get("spec13") != '': new.spec13 = request.form.get("spec13")
        if request.form.get("spec14") != '': new.spec14 = request.form.get("spec14")
        if request.form.get("spec15") != '': new.spec15 = request.form.get("spec15")
        if request.form.get("spec16") != '': new.spec16 = request.form.get("spec16")
        if request.form.get("spec17") != '': new.spec17 = request.form.get("spec17")
        if request.form.get("spec18") != '': new.spec18 = request.form.get("spec18")
        if request.form.get("spec19") != '': new.spec19 = request.form.get("spec19")
        if request.form.get("spec20") != '': new.spec20 = request.form.get("spec20")

        if request.form.get("opisanie") != '': new.opisanie = request.form.get("opisanie")
        new.main = res.id
        
        db.session.add(new)
        db.session.commit()
        return redirect("/adminnspecpro")


@app.route("/adminstatii", methods = ["GET", "POST"])
@login_required
def statii():
    if request.method == "GET":
        all_statii = db.session.query(Post).all()
        #print(all_statii)
        return render_template("vsichkistatii.html", statii = all_statii)


@app.route("/adminstatii<slug>", methods = ["GET", "POST"])
@login_required
def statii1(slug):
    if request.method == "GET":
        statia = db.session.query(Post).filter_by(slug = slug).first()
        return render_template("adminstatia.html", statia = statia)
    if request.method == "POST":
        statia = db.session.query(Post).filter_by(slug = slug).first()

        file = request.files['file']
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        file4 = request.files['file4']
        files = [file, file1, file2, file3, file4]

        title = request.form.get("title")
        category = request.form.get("category")
        slug = request.form.get("slug")

        specList = [request.form.get("spec1"), request.form.get("spec2"), request.form.get("spec3"), request.form.get("spec4"), request.form.get("spec5"), request.form.get("spec6")]
        product_name=[request.form.get("productname"), request.form.get("productname1"), request.form.get("productname2"), request.form.get("productname3"), request.form.get("productname4")]
        content = [request.form.get("content"), request.form.get("content1"), request.form.get("content2"), request.form.get("content3"), request.form.get("content4")]
        spec1answ = [request.form.get("1spec1answ"), request.form.get("1spec2answ"), request.form.get("1spec3answ"), request.form.get("1spec4answ"), request.form.get("1spec5answ"), request.form.get("1spec6answ")]
        spec2answ = [request.form.get("2spec1answ"), request.form.get("2spec2answ"), request.form.get("2spec3answ"), request.form.get("2spec4answ"), request.form.get("2spec5answ"), request.form.get("2spec6answ")]
        spec3answ = [request.form.get("3spec1answ"), request.form.get("3spec2answ"), request.form.get("3spec3answ"), request.form.get("3spec4answ"), request.form.get("3spec5answ"), request.form.get("3spec6answ")]
        spec4answ = [request.form.get("4spec1answ"), request.form.get("4spec2answ"), request.form.get("4spec3answ"), request.form.get("4spec4answ"), request.form.get("4spec5answ"), request.form.get("4spec6answ")]
        spec5answ = [request.form.get("5spec1answ"), request.form.get("5spec2answ"), request.form.get("5spec3answ"), request.form.get("5spec4answ"), request.form.get("5spec5answ"), request.form.get("5spec6answ")]

        for i in range(5):
            if specList[i] != '': statia.spec1
            if specList[i] != '': statia.spec1
            if specList[i] != '': statia.spec1
            if specList[i] != '': statia.spec1
            if specList[i] != '': statia.spec1
            if specList[i] != '': statia.spec1



