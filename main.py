from app import app
from app import db
from statii import statii
from products import products

app.register_blueprint(statii, url_prefix='/statii')
app.register_blueprint(products, url_prefix='/products')

if __name__ == '__main__':
    app.run()