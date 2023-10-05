from App.database import db
from App.models import prerequisites
import json

class Course(db.Model):
    courseCode = db.Column(db.String(8), primary_key=True)
    courseName = db.Column(db.String(25))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    #prerequisites_rel = db.relationship('Prerequisites', foreign_keys='Prerequisites.course_id', backref='prerequisite_rels')
    #prerequisite_for = db.relationship('Prerequisites', foreign_keys='Prerequisites.prereq_code', back_populates='course', overlaps="prerequisites_rel")

    def __init__(self):
        pass
        
        
    def get_prerequisites(self):
        return json.loads(self.prerequisites) if self.prerequisites else []
    
    def get_json(self):
        return{
            'Course Code:': self.courseCode,
            'Course Name: ': self.courseName,
            'Course Rating: ': self.rating,
            'No. of Credits: ': self.credits,
            'Prerequistes: ': self.prerequisites
        }

