from App.database import db

class Course(db.Model):
    courseCode = db.Column(db.String(8), primary_key=True)
    courseName = db.Column(db.String(25))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    prerequisites = db.Column(db.String(24))

    def __init__(self, course_code, course_name, ratings=None, credits=None, prerequisites=None):
        self.courseCode = course_code
        self.course_name = course_name
        self.rating = ratings
        self.credits = credits
        self.prerequisites = prerequisites  
    
    def get_json(self):
        return{
            'Course Code:': self.courseCode,
            'Course Name: ': self.course_name,
            'Course Rating: ': self.rating,
            'No. of Credits: ': self.credits,
            'Prerequistes: ': self.prerequisites
        }

