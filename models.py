from app import db
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = 'post'
    
    mainimage = db.Column(db.String)
    intro = db.Column(db.String)
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    category = db.Column(db.String)
    slug = db.Column(db.String)
    spec1 = db.Column(db.String)
    spec2 = db.Column(db.String)
    spec3 = db.Column(db.String)
    spec4 = db.Column(db.String)
    spec5 = db.Column(db.String)
    spec6 = db.Column(db.String)
    products = db.relationship('Products', backref = 'pageused')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #def __repr__(self):
        #return f'<postid> {self.id} <postsslug> {self.slug} <postcategory> {self.category}'


class Products(Base):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key = True)
    pagesused = db.Column(db.Integer, db.ForeignKey('post.id', ondelete = "CASCADE"))
    #pagesused = db.Column(db.Integer)
    productid = db.Column(db.Integer)
    productname = db.Column(db.String)
    imagepath = db.Column(db.String)
    content = db.Column(db.String)
    spec1answ = db.Column(db.String)
    spec2answ = db.Column(db.String)
    spec3answ = db.Column(db.String)
    spec4answ = db.Column(db.String)
    spec5answ = db.Column(db.String)
    spec6answ = db.Column(db.String)
    store = db.Column(db.String)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Productstore (Base):
    __tablename__ = 'productstore'

    id = db.Column(db.Integer, primary_key = True)
    productname = db.Column(db.String)
    store = db.Column(db.String)
    link = db.Column(db.String)
    lev = db.Column(db.Integer)
    st = db.Column(db.String)
    imagesrc = db.Column(db.String)
    levsale = db.Column(db.Integer)
    stsale = db.Column(db.String)
    specification = db.relationship('Productstorespec', backref = 'spec')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Productstorespec (Base):
    __tablename__ = 'productstorespec'

    id = db.Column(db.Integer, primary_key = True)
    main = db.Column(db.Integer, db.ForeignKey('productstore.id', ondelete = "CASCADE"))
    imagepath1 = db.Column(db.String)
    imagepath2 = db.Column(db.String)
    imagepath3 = db.Column(db.String)
    imagepath4 = db.Column(db.String)
    imagepath5 = db.Column(db.String)
    imagepath6 = db.Column(db.String)
    imagepath7 = db.Column(db.String)
    category = db.Column(db.String) #emag
    
    linker1 = db.Column(db.Integer)
    linker2 = db.Column(db.Integer)
    linker3 = db.Column(db.Integer)
    linker4 = db.Column(db.Integer)
    linker5 = db.Column(db.Integer)
    
    spec1 = db.Column(db.String)
    spec2 = db.Column(db.String)
    spec3 = db.Column(db.String)
    spec4 = db.Column(db.String)
    spec5 = db.Column(db.String)
    spec6 = db.Column(db.String)
    spec7 = db.Column(db.String)
    spec8 = db.Column(db.String)
    spec9 = db.Column(db.String)
    spec10 = db.Column(db.String)
    spec11 = db.Column(db.String)
    spec12 = db.Column(db.String)
    spec13 = db.Column(db.String)
    spec14 = db.Column(db.String)
    spec15 = db.Column(db.String)
    spec16 = db.Column(db.String)
    spec17 = db.Column(db.String)
    spec18 = db.Column(db.String)
    spec19 = db.Column(db.String)
    spec20 = db.Column(db.String)
    opisanie = db.Column(db.String)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
