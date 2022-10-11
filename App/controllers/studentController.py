from App.models import StudentModel
from App.database import db

def create_student(studentId, name):
    newstudent = StudentModel(studentId=studentId, name=name)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

# def get_student_by_studentname(studentname):
#     return student.query.filter_by(name=studentname).first()

# def get_student(id):
#     return student.query.get(id)

def get_all_students():
    return StudentModel.query.all()[0].toJSON()

# def get_all_students_json():
#     students = student.query.all()
#     if not students:
#         return []
#     students = [student.toJSON() for student in students]
#     return students

# def update_student(id, studentname):
#     student = get_student(id)
#     if student:
#         student.studentname = studentname
#         db.session.add(student)
#         return db.session.commit()
#     return None
    