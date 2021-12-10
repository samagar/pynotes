# project/model.py

# from views import db
import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy

class Notes(db.Model):

    __tablename__ = "Notestb"

    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    detail = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Userstb.id') )
 #   posted_date = db.Column(db.Date, default=datetime.datetime.utcnow())     
    posted_date = db.Column(db.String)
    status = db.Column(db.Integer)

    def __init__(self, title, detail, user_id, posted_date, status):
        self.title = title
        self.detail = detail
        self.user_id = user_id
        self.posted_date = posted_date
        self.status = status

    def __repr__(self):
        return '<title {0}>'.format(self.title)
        
class User(db.Model):
    __tablename__ = 'Userstb'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email= db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=True)
    notes = db.relationship('Notes', backref='poster')


    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User{0}>'.format(self.name)