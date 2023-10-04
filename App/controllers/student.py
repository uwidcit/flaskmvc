from App.models import Student, CoursePlan, Program
from App.controllers.coursePlan import addCourse, getCoursePlan, removeCourse
from App.database import db

<<<<<<< HEAD

def create_student(file_path):
    new_student = Student(file_path)
=======
def create_student(student_id, password, name):
    new_student = Student(username=student_id, password=password, name=name)
>>>>>>> fb66afb1efd67da59ad1be48f435f99ff99ed345
    db.session.add(new_student)
    db.session.commit()
    return new_student

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_all_students():
    return Student.query.all()

def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students_json = [student.get_json() for student in students]
    return students_json

def get_course_history(username):
    student = get_student_by_username(username)
    return student.course_history if student else []

<<<<<<< HEAD
def get_program(username):
    student = get_student_by_username(username)
    return student.program if student else ""

def get_nextSemCourses(username):
    student = get_student_by_username(username)
    return student.nextSemCourses if student else []

# def enroll_in_programme(student, programme_id):
#     programme = Program.query.get(programme_id)
#     if programme:
#         student.programmes.append(programme)
#         db.session.add(student)  # Add the student object to the session
#         db.session.commit()
=======
def enroll_in_programme(student_id, programme_id):
    student = get_student(student_id)
    if student:
        programme = Program.query.get(programme_id)
        if programme:
            student.program_id = programme_id
            db.session.add(student)
            db.session.commit()
>>>>>>> fb66afb1efd67da59ad1be48f435f99ff99ed345

def add_course_to_plan(student, course_id):
    addCourse(student,course_id)
    return

def remove_course_from_plan(student, course_id):
    removeCourse(student,course_id)
    return

def view_course_plan(student):
    plan=getCoursePlan(student.id)
    return plan

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
