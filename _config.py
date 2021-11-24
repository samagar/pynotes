import os

# Grab the folder where this script lives
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasknote.db'
USERNAME = 'sandeep'
PASSWORD = 'sandeep'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'myprecious'

# define the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH