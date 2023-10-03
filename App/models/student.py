from App.models import User  
from App.database import db
import json

class Student(User):
    id = db.Column( db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))
    course_history = db.Column(db.String(500))
    #CoursePlan -> nextSemCourses
    nextSemCourses = db.Column(db.String(50))
    program = db.Column(db.String(50))


    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            username = lines[0].strip()
            password = lines[1].strip()
            super.__init__(username, password)
            self.id = lines[0].strip()
            self.name = lines[2].strip()
            self.program = lines[3].strip()
            self.course_history = json.dumps(lines[4].strip().split(','))

    def str_course_history(self):
        return json.loads(self.course_history) if self.course_history else [] 

    def get_json(self):
        return{
            'student_id': self.id,
            'name': self.name,
            'course history': self.course_history,
            'next semester courses': self.nextSemCourses,
            'program' : self.program
        }

