from App.models import User  
from App.database import db
import json

class Student(User):
    id = db.Column( db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))
    course_history = db.Column(db.String(500))
    #CoursePlan -> nextSemCourses
    nextSemCourses = db.Column(db.String(50))
    program_id = db.Column(db.String(10), db.ForeignKey('program.id'))
    associated_program = db.relationship('Program', back_populates='students', overlaps="program")

<<<<<<< HEAD

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
=======
    def __init__(self, username, password, name, course_history=None, next_sem_courses=None, program_id=None):
        super().__init__(username, password)
        self.name = name
        self.course_history = course_history
        self.nextSemCourses = next_sem_courses
        self.program_id = program_id
>>>>>>> development

    def str_course_history(self):
        return json.loads(self.course_history) if self.course_history else [] 

<<<<<<< HEAD
    def get_json(self):
=======
    def str_courseHistory(self):
        return json.loads(self.course_history) if self.course_history else [] 

def get_json(self):
>>>>>>> development
        return{
            'student_id': self.id,
            'name': self.name,
            'course history': self.course_history,
            'next semester courses': self.nextSemCourses,
            'program' : self.program
        }

