import sqlite3
import os

dbcon = sqlite3.connect('schedule.db')
with dbcon:
    cursor = dbcon.cursor()
    cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, NAME TEXT NOT NULL)")  # create table students