from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import ForeignKey, create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests
import boto3
import uuid
import json
import urllib.request
import os
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from config import Config
print(os.getenv("DATABASE_URI"))
engine = create_engine(os.getenv("DATABASE_URI"))
conn = engine.connect()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "secret key"
print(os.getenv('AWS_SECRET_ACCESS_KEY'))
Session(app)

db = SQLAlchemy(app)
from models import *
Base.metadata.create_all(engine)
base = declarative_base()
#Productstorespec.__table__.drop(engine)
#Productstore.__table__.drop(engine)
#Products.__table__.drop(engine)
#Post.__table__.drop(engine)

from scraping import scrapeTechnopolis, scrapeEmag

with app.app_context():
    #db.create_all()
    pass

BUCKET_NAME = "evtino"
#s3 = boto3.client("s3", aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))
s3 = boto3.resource("s3")

ALLOWED_CATEGORIES = set(['smartphone', 'laptop', ''])
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkandSaveFile(files):
    files1=[]
    for file in files:
            new_filename = ''
            if file.filename == '':
                message = 'No image selected for uploading'
        
            if file and allowed_file(file.filename):
                new_filename =  save_file(file)
                files1.append(new_filename)
            else:
                files1.append("")
                message = 'Allowed image types are - png, jpg, jpeg, gif'
    return files1


def checkandSaveFileLink(files):
    files1=[]
    for file in files:
        if file.filename != '' and allowed_file(file.filename):
            new_filename = save_file(file)
            emag_filename = f"https://evtino.s3.eu-central-1.amazonaws.com/{new_filename}"
            files1.append(emag_filename)
        else:
            files1.append('')
    return files1

def saveProductsStatii(iterable, products, spec):
    index1 = 0
    for i in iterable:
            if i != "":
                setattr(products[index1], spec, i)
            index1 += 1
    return products

def newProductsStatii(iterable, products, spec):
    index1 = 0
    for i in iterable:
            setattr(products[index1], spec, i)
            index1 += 1
    return products


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

@app.errorhandler(500)
def sessionerror():
    print("ankara")
    return redirect()


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()
        postsall = sessiondb.query(Post).limit(5).all()

        with open("./static/top5.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            print(type(data))
        sessiondb.close()
        return render_template("homepage.html", dict1 = data, postsall= postsall)
    

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
        return render_template("din.html")
        

@app.route("/adminnapishi", methods = ["GET", "POST"])
@login_required
def napishi():
    if request.method == "GET":
        return render_template("din-napishi.html")
    if request.method == "POST":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()



        files1 =[]
        file = request.files.getlist('file')
        #print(file)
        #file1 = request.files['file1']
        #file2 = request.files['file2']
        #file3 = request.files['file3']
        #file4 = request.files['file4']
        #file5 = request.files['file-main']
        #files = [file, file1, file2, file3, file4, file5]

        intro = request.form.get("intro")
        title = request.form.get("title")
        category = request.form.get("category")
        slug = request.form.get("slug")

        specList = [request.form.get("spec1"), request.form.get("spec2"), request.form.get("spec3"), request.form.get("spec4"), request.form.get("spec5"), request.form.get("spec6")]
        # id1 = [request.form.get("id"), request.form.get("id1"), request.form.get("id2"), request.form.get("id3"), request.form.get("id4")]
        # product_name=[request.form.get("productname"), request.form.get("productname1"), request.form.get("productname2"), request.form.get("productname3"), request.form.get("productname4")]
        # content = [request.form.get("content"), request.form.get("content1"), request.form.get("content2"), request.form.get("content3"), request.form.get("content4")]
        # spec1answ = [request.form.get("1spec1answ"), request.form.get("1spec2answ"), request.form.get("1spec3answ"), request.form.get("1spec4answ"), request.form.get("1spec5answ"), request.form.get("1spec6answ")]
        # spec2answ = [request.form.get("2spec1answ"), request.form.get("2spec2answ"), request.form.get("2spec3answ"), request.form.get("2spec4answ"), request.form.get("2spec5answ"), request.form.get("2spec6answ")]
        # spec3answ = [request.form.get("3spec1answ"), request.form.get("3spec2answ"), request.form.get("3spec3answ"), request.form.get("3spec4answ"), request.form.get("3spec5answ"), request.form.get("3spec6answ")]
        # spec4answ = [request.form.get("4spec1answ"), request.form.get("4spec2answ"), request.form.get("4spec3answ"), request.form.get("4spec4answ"), request.form.get("4spec5answ"), request.form.get("4spec6answ")]
        # spec5answ = [request.form.get("5spec1answ"), request.form.get("5spec2answ"), request.form.get("5spec3answ"), request.form.get("5spec4answ"), request.form.get("5spec5answ"), request.form.get("5spec6answ")]
        products = [Products(), Products(), Products(), Products(), Products()]
        specifications = ["spec1answ", "spec2answ", "spec3answ", "spec4answ", "spec5answ", "spec6answ", "content", "productname"]
        for spec in specifications:
            products = newProductsStatii(request.form.getlist(spec), products, spec)
        
        
        files1 = checkandSaveFile(file)
        print(files1)
        start = 1
        post_new = Post(mainimage = files1[0], intro = intro, slug = slug, title = title, category = category, spec1 = specList[0], spec2 = specList[1], spec3 = specList[2], spec4 = specList[3], spec5 = specList[4], spec6 = specList[5])
        sessiondb.add(post_new)
        sessiondb.commit()

        obj = sessiondb.query(Post).order_by(Post.id.desc()).first()

        for i in products:
            i.imagepath = files1[start]
            start+=1
            i.pagesused = obj.id
            sessiondb.add(i)
        
        # products = Products(productid = id1[0], store = "emag", pageused = obj, productname = product_name[0], imagepath = files1[0], content = content[0], spec1answ = spec1answ[0], spec2answ = spec1answ[1], spec3answ = spec1answ[2], spec4answ = spec1answ[3], spec5answ = spec1answ[4], spec6answ = spec1answ[5])
        # products1 = Products(productid = id1[1], store = "emag", pageused = obj, productname = product_name[1], imagepath = files1[1], content = content[1], spec1answ = spec2answ[0], spec2answ = spec2answ[1], spec3answ = spec2answ[2], spec4answ = spec2answ[3], spec5answ = spec2answ[4], spec6answ = spec2answ[5])
        # products2 = Products(productid = id1[2], store = "emag", pageused = obj, productname = product_name[2], imagepath = files1[2], content = content[2], spec1answ = spec3answ[0], spec2answ = spec3answ[1], spec3answ = spec3answ[2], spec4answ = spec3answ[3], spec5answ = spec3answ[4], spec6answ = spec3answ[5])
        # products3 = Products(productid = id1[3], store = "emag", pageused = obj, productname = product_name[3], imagepath = files1[3], content = content[3], spec1answ = spec4answ[0], spec2answ = spec4answ[1], spec3answ = spec4answ[2], spec4answ = spec4answ[3], spec5answ = spec4answ[4], spec6answ = spec4answ[5])
        # products4 = Products(productid = id1[4], store = "emag", pageused = obj, productname = product_name[4], imagepath = files1[4], content = content[4], spec1answ = spec5answ[0], spec2answ = spec5answ[1], spec3answ = spec5answ[2], spec4answ = spec5answ[3], spec5answ = spec5answ[4], spec6answ = spec5answ[5])
        # products_list = [products, products1, products2, products3, products4]
        #
        # for i in products:
        #     sessiondb.commit(i)
        #sessiondb.close()
        prod = sessiondb.query(Products).filter_by(pageused = obj).all()
        print(prod)
        sessiondb.close()
        return render_template("statii.html", statia = post_new, productslist = prod)

@app.route("/adminproduct", methods = ["GET", "POST"])
@login_required
def product():
    if request.method == "GET":
        return render_template("adminproduct.html")
    if request.method == "POST":
        link = request.form.get("link")
        storename = str(request.form.get("storename"))
        if storename == "emag":
            scrapeEmag(link)

        if storename == "technopolis":
            scrapeTechnopolis(link)
            
        return redirect("/adminnspecpro")


@app.route("/adminnspecpro", methods = ["GET", "POST"])
@login_required
def prodspec():
    if request.method == "GET": 
        Session = sessionmaker(bind=engine)
        sessiondb = Session()

        res = sessiondb.query(Productstore).all()
        sessiondb.close()
        return render_template("productspec.html", products1 = res)

@app.route("/adminnspecpro<id>", methods = ["GET", "POST"])
@login_required
def prodspec1(id):
    if request.method == "GET":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()

        product = sessiondb.query(Productstore).filter_by(id = id).first()
        sessiondb.close()
        return render_template("admaddprodspec.html", product = product)

    if request.method == "POST":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()
    
        files1 = []

        res = sessiondb.query(Productstore).filter_by(id = id).first()
        new = sessiondb.query(Productstorespec).filter_by(main = res.id).first()

        if not new:
            new = Productstorespec()
        files = [request.files['file1'], request.files['file2'], request.files['file3'], request.files['file4'], request.files['file5'], request.files['file6'], request.files['file7'], request.files['mainimage']]

        files1 = checkandSaveFileLink(files)

        items = request.form.items() 
        for item in items:
            if item[1] != "":
                setattr(new, item[0], item[1])

        
        for i in len(files1) - 1:
            if files1[i] != "":
                string = f"imagepath{i}"
                setattr(new, string, i)
        # if files1[0] != '':
        #     new.imagepath1 = files1[0]
        # if files1[1] != '':
        #     new.imagepath2 = files1[1]
        # if files1[2] != '':
        #     new.imagepath3 = files1[2]
        # if files1[3] != '':
        #     new.imagepath4 = files1[3]
        # if files1[4] != '':
        #     new.imagepath5 = files1[4]
        # if files1[5] != '':
        #     new.imagepath6 = files1[5]
        # if files1[6] != '':
        #     new.imagepath7 = files1[6]
        

        if files1[7] != '': res.imagesrc = files1[7]
        new.main = res.id
        sessiondb.add(new)
        sessiondb.commit()
        sessiondb.close()
        return redirect("/adminnspecpro")


@app.route("/adminstatii", methods = ["GET", "POST"])
@login_required
def statii():
    if request.method == "GET":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()

        all_statii = sessiondb.query(Post).all()
        sessiondb.close()
        return render_template("vsichkistatii.html", statii = all_statii)


@app.route("/adminstatii<slug>", methods = ["GET", "POST"])
@login_required
def statii1(slug):
    if request.method == "GET":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()

        statia = sessiondb.query(Post).filter_by(slug = slug).first()
        products = sessiondb.query(Products).filter_by(pageused = statia).all()

        sessiondb.close()
        return render_template("adminstatia.html", statia = statia, products=products)
    
    if request.method == "POST":
        Session = sessionmaker(bind=engine)
        sessiondb = Session()
        statia = sessiondb.query(Post).filter_by(slug = slug).first()
        products = sessiondb.query(Products).filter_by(pageused = statia).all()

        file = request.files['file']
        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']
        file4 = request.files['file4']
        files = [file, file1, file2, file3, file4]

        specifications = ["spec1answ", "spec2answ", "spec3answ", "spec4answ", "spec5answ", "spec6answ", "content", "productname"]
        for spec in specifications:
            products = saveProductsStatii(request.form.getlist(spec), products, spec)

        files1 = checkandSaveFile(files1)
        title = request.form.get("title")
        category = request.form.get("category")
        slug = request.form.get("slug")
        intro = request.form.get('intro')
        if category != '': statia.category = category
        if title != '': statia.title = title
        if slug != '': statia.slug = slug
        if intro != '': statia.intro = intro   
        
        sessiondb.commit()
        sessiondb.close()
        return redirect("/adminstatii")




