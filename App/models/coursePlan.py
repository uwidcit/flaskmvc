from flask_login import UserMixin
from App.database import db
import json

class CoursePlan(db.Model,UserMixin):
    planId=db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)    
    courses=db.Column(db.String(200), nullable=True)
=======
    studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)
    courses=db.Column(db.String(100), nullable=True)
    #student=db.relationship('Student', db.backref('CoursePlan'))
    student = db.relationship('Student', backref=db.backref('course_plans', uselist=True))
>>>>>>> fb66afb1efd67da59ad1be48f435f99ff99ed345
    
    
    def __init__(self, studentId):
        self.studentId = studentId
        self.courses=""

    def get_json(self):
        return{
            'planId': self.planId,
            'studentId': self.studentId,
            'courses': self.courses
        }

    def __repr__(self):
        return f'<CoursePlan {self.planId} - {self.studentId} - {self.courses}>'


