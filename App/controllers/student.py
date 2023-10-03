from App.models import Student, CoursePlan, Program
from App.database import db

def create_student(file_path):
    new_student = Student(file_path)
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

# def add_course_to_plan(student, course_id):
#     #Ashely needed here 
#     course = CoursePlan.query.get(course_id)
#     if course:
#         student.courses.append(course)
#         db.session.add(student)  
#         db.session.commit()

# def remove_course_from_plan(student, course_id):
#     #Ashely needed here
#     course = CoursePlan.query.get(course_id)
#     if course:
#         student.courses.remove(course)
#         db.session.add(student)  # Add the student object to the session
#         db.session.commit()

# def view_course_plan(student):
#     #Ashely needed here
#     return [course.get_json() for course in student.courses]

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
