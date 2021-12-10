# create database

from views import db
from models import Notes
from datetime import date

# create the database and the db table
db.create_all()
# insert data
db.session.add(Notes("Note1","Note Detail1","admin",date(2020, 9, 22),1))
db.session.add(Notes("Note2","Note Detail2","admin",date(2021, 9, 22),1))

# commit the changes
db.session.commit()