import os
import sys
import sqlite3


def courses_not_done():
    cursor.execute("SELECT COUNT(id) FROM courses")
    num_of_courses = cursor.fetchone()
    return num_of_courses[0] > 0


# TODO-

databaseexisted = os.path.isfile('schedule.db')

dbcon = sqlite3.connect('schedule.db')
with dbcon:
    cursor = dbcon.cursor()

    iteration_number = 0
    while databaseexisted and courses_not_done():

        # decrease all courses time
        cursor.execute('UPDATE classrooms '
                       'SET current_course_time_left = current_course_time_left - 1 '
                       'WHERE current_course_time_left >0')
        dbcon.commit();
        # print and delete all courses that are finished
        cursor.execute(("SELECT co.course_name,cl.location "
                        "FROM "
                        "classrooms as cl, "
                        "courses as co "
                        "WHERE cl.current_course_time_left=0 AND cl.current_course_id = co.id"))

        done_courses = cursor.fetchall()
        for element in done_courses:
            print("(" + str(iteration_number) + ") " + element[1] + ": " + element[0] + " is done")
        cursor.execute("SELECT current_course_id "
                       "FROM classrooms "
                       "WHERE current_course_time_left=0 "
                       "AND current_course_id!=0")
        delete_this = cursor.fetchall();
        for i in range(0, len(delete_this)):
            id = delete_this[i]
            cursor.execute("DELETE "
                           "FROM courses "
                           "WHERE id=?", (id))
        # update classroom that now available
        cursor.execute("UPDATE classrooms "
                       "SET current_course_id = 0 "
                       "WHERE current_course_time_left=0")
        dbcon.commit();
        # print courses that are occupied
        cursor.execute(("SELECT co.course_name,cl.location "
                        "FROM classrooms as cl "
                        "JOIN courses as co "
                        "ON cl.current_course_time_left>0 AND cl.current_course_id = co.id"))
        occupied_classrooms = cursor.fetchall()
        for element in occupied_classrooms:
            print("(" + str(iteration_number) + ") " + element[1] + ": occupied by " + element[0])

        # add courses to classrooms
        cursor.execute("SELECT id,location FROM classrooms WHERE current_course_time_left=0")
        list_of_free_classroom = cursor.fetchall()
        for i in range(0, len(list_of_free_classroom)):
            id = list_of_free_classroom[i][0]
            cursor.execute("SELECT id, course_length,course_name FROM courses WHERE class_id=? ", (id,))
            one_course = cursor.fetchone()
            if one_course is not None:
                print("(" + str(iteration_number) + ") " + list_of_free_classroom[i][1] + ": " + one_course[2]
                      + " is schedule to start")
                cursor.execute("UPDATE classrooms  "
                               "SET current_course_id = ?, "
                               "current_course_time_left = ? "
                               "WHERE id= ?", (one_course[0], one_course[1], id,))



        dbcon.commit();
        iteration_number = iteration_number + 1
