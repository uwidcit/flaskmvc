from .user import User  # Import the User class from user.py
from App.database import db
import json

class Student(User):
    id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))
    course_history = db.Column(db.String(500))
    nextSemCourses = db.Column(db.String(50))
    program_id = db.Column(db.String(10), db.ForeignKey('program.id'))
    associated_program = db.relationship('Program', back_populates='students', overlaps="program")


# def __init__(self, file_path):
#         try:
#             with open(file_path, 'r') as file:
#                 lines = file.readlines()
#                 self.name = lines[0].strip()
#                 self.level1_credits = lines[1].strip()
#                 self.level1_courses = json.dumps(lines[2].strip().split(','))
#                 self.core_credits = lines[3].strip()
#                 self.core_courses = json.dumps(lines[4].strip().split(','))
#                 self.elective_credits = lines[5].strip()
#                 self.elective_courses = json.dumps(lines[6].strip().split(','))
#                 self.foun_credits = lines[7].strip()
#                 self.foun_courses = json.dumps(lines[8].strip().split(','))
                 
#         except FileNotFoundError:
#             print("File not found.")

#         except Exception as e:
#             print(f"An error occurred: {e}")

def __init__(self, username, password, name, course_history=None, next_sem_courses=None, program_id=None):
        # Call the parent class's __init__ method
        super().__init__(username, password)

        # Initialize the additional fields
        self.name = name
        self.course_history = course_history
        self.nextSemCourses = next_sem_courses
        self.program_id = program_id
        #program_id = db.Column(db.String(10), db.ForeignKey('program.id'))
        #program = db.relationship('Program', back_populates='students')

        
        #with open(file_path, 'r') as file:
        #    lines = file.readlines()


        # course History, courses, programmes using a file, 

# needed for nextSemCourses and Course history 
# def get_prerequisites(self):
#     return json.loads(self.prerequisites) if self.prerequisites else [] 

def get_json(self):
        return{
            'student_id': self.id,
            'name': self.name,
            'course history': self.course_history,
            'next semester courses': self.nextSemCourses,
            'program' : self.program
        }

