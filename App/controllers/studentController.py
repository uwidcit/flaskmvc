from App.models import StudentModel
from App.models import Reviews
from App.database import db

def create_student(studentId, name):
    newstudent = StudentModel(studentId=studentId, name=name)
    db.session.add(newstudent)
    db.session.commit()
    return newstudent

def create_review( message, id, upvote, downvote):
    newReview = Reviews( message=message, studentId = id, upvote=upvote, downvote=downvote)
    db.session.add(newReview)
    db.session.commit()
    return newReview



# def get_student_by_studentname(studentname):
#     return student.query.filter_by(name=studentname).first()

# def get_student(id):
#     return student.query.get(id)

def get_all_students():
    students = StudentModel.query.all()
    newReviews = []
    for student in students:
        for review in student.reviews:
            review = review.toJSON()
            newReviews.append(review)
            print(newReviews)
        student = student.toJSON()
        student['reviews'] = newReviews
        print(student)
    return student 



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
    