import json
from App.database import db 

class OfferedCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offered = db.Column(db.String(10))

    def __init__(self, courseCode):
        self.offered = courseCode
       
    def get_json(self):
        return{
            'Course Code:': self.offered
        }
