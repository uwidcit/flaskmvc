from App.models import StudentModel
from App.models import Reviews
from App.database import db
import json
from flask import jsonify

def validate_vote(data):
    if( data['upvote'] > 1 or data['upvote']< 0):
        return False,jsonify({'message': f"Invalid value for upvote: {data['upvote']}"})
    if( data['downvote'] > 1 or data['downvote']< 0):
        return False,jsonify({'message': f"Invalid value for downvote: {data['downvote']}"})
    return True,""

def validate_student_id(studentId):
    if(isinstance(studentId,int)):
        return True,""
    return False,jsonify({'message': f"Invalid value for studentId: {studentId}"})
   

def create_student(studentId, name):
    student = StudentModel.query.filter_by(studentId=studentId).first()
    if(student):
        return False
    newstudent = StudentModel(studentId=studentId, name=name)
    db.session.add(newstudent)
    db.session.commit()
    return True

def create_review( message, studentId, upvote, downvote):
    if(upvote == 1 and downvote == 1):
        return False
    else:
        newReview = Reviews( message=message, studentId = studentId, upvote=upvote, downvote=downvote)
        db.session.add(newReview)
        db.session.commit()
        if(upvote != 0 and downvote != 0):
            karma_calc(id)
        return newReview
            
        
def update_review(id, upvote, downvote):
    
    if(upvote == 1 and downvote == 1):
        return False
    else:
        review = Reviews.query.get(id)
        print(review.toJSON())
        review.upvote+=upvote
        review.downvote+=downvote
        db.session.commit()
        if(upvote != 0 and downvote != 0):
            karma_calc(review.studentId)
        print(review.toJSON())
        return review
        

def karma_calc(studentId):
    reviews = Reviews.query.filter_by(studentId=studentId).all()
    upvotes = 0
    downvotes = 0 
    for review in reviews:
        # print(review.toJSON())
        upvotes+=review.upvote
        downvotes+=review.downvote
    if(upvotes == 0 ):
        upvotes = 1
    if(downvotes == 0 ):
        downvotes = 1
    karma = upvotes/downvotes * 100
    student = StudentModel.query.filter_by(studentId=studentId).first()
    student.karma = karma
    db.session.commit()
    print(karma)
    print("calculated Karma")
    # print(student.toJSON())
    return True
    #return json.dumps(reviews)

# def update_student(name):
#     student = StudentModel.query.get(studentId)
#     print(student)
#     student.name = name
#     db.session.commit()
    # if student :
        # student.name = name
        # db.session.commit()
    #     return student.name
    
    # return f'{studentId} user not found'


# def get_student_by_studentname(studentname):
#     return student.query.filter_by(name=studentname).first()

def get_student(studentId):
    #student = StudentModel.query.(studentId)
    student = StudentModel.query.filter_by(studentId=studentId).first()
    return student

def get_student_toJSON(studentId):
    #student = StudentModel.query.(studentId)
    student = StudentModel.query.filter_by(studentId=studentId).first()
    #print(student.toJSON())
    return student.toJSON()

def update_student(studentId, name):
    student = get_student(studentId)
    #print(student.name)
    if student:
        student.name = name
        print(student.name)
        db.session.add(student)
        return db.session.commit()
    return False

def get_all_students():
    students = StudentModel.query.all()
    newReviews = []
    newStudents = []
    for student in students:
        for review in student.reviews:
            review = review.toJSON()
            newReviews.append(review)
            print(newReviews)
        student = student.toJSON()
        student['reviews'] = newReviews
        newReviews = []
        newStudents.append(student)
    print(newStudents)
    return newStudents 



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
    