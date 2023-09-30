from App.database import db
import json

class Course(db.Model):
    courseCode = db.Column(db.String(8), primary_key=True)
    courseName = db.Column(db.String(25))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    prerequisites = db.Column(db.String(24))

    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.courseCode = lines[0].strip()
                self.courseName = lines[1].strip()
                self.credits = lines[2].strip()
                self.rating = lines[3].strip()
                self.prerequisites = json.dumps(lines[4].strip().split(','))  
        
        except FileNotFoundError:
            print("File not found.")

        except Exception as e:
            print(f"An error occurred: {e}")
        
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

