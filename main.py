from app import app
from app import db
from blueprint import statii

app.register_blueprint(statii, url_prefix='/statii')

if __name__ == '__main__':
    app.run()