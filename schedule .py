import os
import sqlite3

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


def courses_not_done():
    cursor.execute("SELECT COUNT(id) FROM courses")
    num_of_courses = cursor.fetchone()
    return num_of_courses[0] > 0


def assign_course(class_id, location):
    cursor.execute('SELECT id, course_name, course_length, student, number_of_students '
                   'FROM courses '
                   'WHERE class_id = ?', (class_id,))
    course = cursor.fetchone()
    if course is not None:
        print("(" + str(iteration_number) + ") " + location + ": " + course[1] + " is schedule to start")
        cursor.execute('UPDATE classrooms '
                       'SET current_course_id = ?, '
                       'current_course_time_left = ? '
                       'WHERE id = ?', (course[0], course[2], class_id))
        cursor.execute('UPDATE students '
                       'SET count = count - ? '
                       'WHERE grade = ?', (course[4], course[3]))


def decreases_count(course_id, location, num):
    cursor.execute('SELECT course_name '
                   'FROM courses '
                   'WHERE id = ?', (course_id,))
    course_name = cursor.fetchone()
    if course_name is not None:
        if num > 1:
            print("(" + str(iteration_number) + ") " + location + ": occupied by " + course_name[0])
        cursor.execute('UPDATE classrooms '
                       'SET current_course_time_left = current_course_time_left - 1 '
                       'WHERE current_course_id = ?', (course_id,))
    cursor.execute('SELECT current_course_time_left '
                   'FROM classrooms '
                   'WHERE current_course_id = ?', (course_id,))
    left = cursor.fetchone()
    if left[0] != 0:
        cursor.execute('UPDATE classrooms '
                       'SET current_course_time_left = 0'
                       'WHERE current_course_id = ?', (course_id,))



def remove_course(course_id, location):
    cursor.execute('SELECT course_name '
                   'FROM courses '
                   'WHERE id = ?', (course_id,))
    course_name = cursor.fetchone()
    if course_name is not None:
        print("(" + str(iteration_number) + ") " + location + ": " + course_name[0] + " is done")
        cursor.execute('DELETE '
                       'FROM courses '
                       'WHERE id = ?', (course_id,))


databaseexisted = os.path.isfile('schedule.db')

dbcon = sqlite3.connect('schedule.db')

with dbcon:
    cursor = dbcon.cursor()

    iteration_number = 0
    while databaseexisted and courses_not_done():
        cursor.execute('SELECT * '
                       'FROM classrooms')
        classrooms = cursor.fetchall()
        for one_classroom in classrooms:
            if one_classroom[3] == 0:
                assign_course(one_classroom[0], one_classroom[1])
            elif one_classroom[3] > 0:
                decreases_count(one_classroom[2], one_classroom[1], one_classroom[3])
            cursor.execute('SELECT * '
                           'FROM classrooms '
                           'WHERE id = ?', (one_classroom[0],))
            one_classroom = cursor.fetchone();
            if one_classroom[3] == 0:
                remove_course(one_classroom[2], one_classroom[1])
                assign_course(one_classroom[0], one_classroom[1])
        print_table()
        iteration_number = iteration_number + 1

dbcon.commit()

