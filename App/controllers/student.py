from App.models import Student, CoursePlan, Program
from App.controllers import (get_program_by_name)
from App.database import db

def create_student(student_id, password, name, programname):
    program = get_program_by_name(programname)
    if program:
        new_student = Student(student_id, password, name, program.id)
        db.session.add(new_student)
        db.session.commit()
        print("Student successfully created")
    else:
        print("Program doesn't exist")

def get_student_by_id(ID):
    return Student.query.filter_by(id=ID).first()

def get_student(id):
    return Student.query.get(id)

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def update_student(id, username):
    student = get_student_by_id(id)
    if student:
        student.username = username
        db.session.add(student)
        db.session.commit()
        return student

def enroll_in_programme(student_id, programme_id):
    student = get_student_by_id(student_id)
    if student:
        programme = Program.query.get(programme_id)
        if programme:
            student.program_id = programme_id
            db.session.add(student)
            db.session.commit()

def add_course_to_plan(student, course_id):
    addCourse(student,course_id)
    return

def remove_course_from_plan(student, course_id):
    removeCourse(student,course_id)
    return

def view_course_plan(student):
    plan=getCoursePlan(student.id)
    return plan

def verify_student(username):
    student=Student.query.filter_by(id=username).first()
    if student:
        return True
    return False

# def add_courses_from_file(student, file_path):
#     try:
#         with open(file_path, 'r') as file:
#             course_ids = [line.strip() for line in file.readlines()]
#             for course_id in course_ids:
#                 add_course_to_plan(student, course_id)
#         db.session.commit()  # Commit the changes after adding courses
#     except FileNotFoundError:
#         return "File not found."
#     except Exception as e:
#         return str(e)
