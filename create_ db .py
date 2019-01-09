import sqlite3
import os

databaseexisted = os.path.isfile('schedule.db')

dbcon = sqlite3.connect('schedule.db')
with dbcon:
    cursor = dbcon.cursor()
    cursor.execute("CREATE TABLE courses(id INTEGER PRIMARY KEY, course_name TEXT NOT NULL, "
                   "student TEXT NOT NULL, number_of_students INTEGER NOT NULL,"
                   " class_id INTEGER REFERENCES classrooms(id), number_of_students INTEGER NOT NULL)")  # create table courses
    cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL)")  # create table students
    cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY, location TEXT NOT NULL, "
                   "current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL)")  # create table classrooms
