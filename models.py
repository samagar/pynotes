# project/db_create.py

from datetime import date

import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

    # get a cursor object used to execute SQL commands
    c = connection.cursor()

    # create Notes table
    c.execute("""CREATE TABLE Notes(note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,detail TEXT NOT NULL, posted_date TEXT NOT NULL, 
        UserId INTEGER,
        status INTEGER,
        FOREIGN KEY(UserId) REFERENCES Users(user_id))""")

    # insert dummy data into the notes table
    c.execute(
        'INSERT INTO Notes (title, detail, posted_date, status)'
        'VALUES("Test","test","03/25/2020", 1)'
    )
    c.execute(
        'INSERT INTO Notes (title, detail, posted_date, status)'
        'VALUES("Test2","test2","03/25/2021", 1)'
    )

    # create Users table
    c.execute("""CREATE TABLE Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,email TEXT NOT NULL, 
        password TEXT NOT NULL,
        note_id TEXT,
        FOREIGN KEY(note_id) REFERENCES Notes(note_id)
        )""")

    # insert dummy data into the User table
    c.execute(
        'INSERT INTO Users (name, email, password)'
        'VALUES("Test","Test@gmail.com", "Test")'
    )
