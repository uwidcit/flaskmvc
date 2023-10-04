from App.database import db
import json
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    level1_credits = db.Column(db.Integer)
    level1_courses = db.Column(db.String(200))
    core_credits = db.Column(db.Integer)
    core_courses = db.Column(db.String(200))
    elective_credits = db.Column(db.Integer)
    elective_courses = db.Column(db.String(200))
    foun_credits = db.Column(db.Integer)
    foun_courses = db.Column(db.String(30))
    students = db.relationship('Student', backref='program', lazy=True)

    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip()
                self.level1_credits = lines[1].strip()
                self.level1_courses = json.dumps(lines[2].strip().split(','))
                self.core_credits = lines[3].strip()
                self.core_courses = json.dumps(lines[4].strip().split(','))
                self.elective_credits = lines[5].strip()
                self.elective_courses = json.dumps(lines[6].strip().split(','))
                self.foun_credits = lines[7].strip()
                self.foun_courses = json.dumps(lines[8].strip().split(','))
                 
        except FileNotFoundError:
            print("File not found.")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def str_level1_courses(self):
        return json.loads(self.level1_courses) if self.level1_courses else []

    def str_core_courses(self):
        return json.loads(self.core_courses) if self.core_courses else []
    
    def str_elective_courses(self):
        return json.loads(self.elective_courses) if self.elective_courses else []
    
    def str_foun_courses(self):
        return json.loads(self.foun_courses) if self.foun_courses else []


    def get_json(self):
        return{
            'Program ID:': self.id,
            'Program Name: ': self.name,
            'Level I Credits: ': self.level1_credits,
            'Level I Courses: ': self.level1_courses,
            'Core Credits: ': self.core_credits,
            'Core Courses: ': self.core_courses,
            'Elective Credits ': self.elective_credits,
            'Elective Courses: ': self.elective_courses,
            'Foundation Credits: ': self.foun_credits,
            'Foundation Courses: ': self.foun_courses
        }
       