from sqlalchemy.orm import sessionmaker
from psycopg2 import OperationalError
from flask import request, redirect

def sessionMake(engine):
    try:
        Session = sessionmaker(bind=engine)
        sessiondb = Session()
    except OperationalError as err:
        current_url = request.full_path
        return redirect(current_url)
    return sessiondb