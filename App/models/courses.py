from App.database import db
import json

class Course(db.Model):
    courseCode = db.Column(db.String(8), primary_key=True)
    courseName = db.Column(db.String(25))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    prerequisites = db.Column(db.String(24))

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

