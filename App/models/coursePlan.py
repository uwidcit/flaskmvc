from flask_login import UserMixin
from App.database import db
import json

class CoursePlan(db.Model,UserMixin):
    planId=db.Column(db.Integer, primary_key=True)
    #studentId=db.Column(db.Integer,  db.foreignkey('student.id'), nullable=False)
    courses = db.Column((db.String(200)), nullable=True)
    #student=db.relationship('Student', db.backref('CoursePlan'))
    
    def __init__(self, studentId, courses=None):
        self.studentId = studentId
        self.courses=json.dumps(courses)

    def get_json(self):
        return{
            'planId': self.planId,
            'studentId': self.studentId,
            'courses': self.courses
        }

    def __repr__(self):
        return f'<CoursePlan {self.planId} - {self.studentId} - {self.courses}>'


