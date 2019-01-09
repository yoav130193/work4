import sqlite3
import os
import sys

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


def add_student(arguments):
    cursor.execute("INSERT INTO students VALUES(?,?)", (arguments[1], arguments[2]))


def add_classroom(arguments):
    cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)", (arguments[1], arguments[2], 0, 0))


def add_course(arguments):
    cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)",
                   (arguments[1], arguments[2], arguments[3], arguments[4], arguments[5], arguments[6]))


with open(sys.argv[1], 'r') as config:
    lines = config.read().split('\n')
    for i in range(0, len(lines)):
        arguments = lines[i].split(',')
        if arguments[0] == 'S':
            add_student(arguments)
        elif arguments[0] == 'R':
            add_classroom(arguments)
        elif arguments[0] == 'C':
            add_course(arguments)


def print_table():
    print('courses')
    cursor.execute("SELECT * FROM courses")
    list = cursor.fetchall()
    for element in list:
        print(str(element))
    print('classrooms')
    cursor.execute("SELECT * FROM classrooms")
    list = cursor.fetchall()
    for element in list:
        print(str(element))
    print('students')
    cursor.execute("SELECT * FROM students")
    list = cursor.fetchall()
    for element in list:
        print(str(element))

print_table()