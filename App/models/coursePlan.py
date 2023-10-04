from flask_login import UserMixin
from App.database import db
import json

class CoursePlan(db.Model,UserMixin):
    planId=db.Column(db.Integer, primary_key=True)
    studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)    
    courses=db.Column(db.String(200), nullable=True)
    
    
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


