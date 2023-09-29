from App.database import db
from App.models import courses
import json
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    coursesCodes = db.Column(db.String(150))

    def __init__(self, file_path):

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.name = lines[0].strip()
                self.courseCodes = [code.strip() for code in lines[1:]]  
                #self.courseCodes = json.dumps([code.strip() for code in lines[1:]])
                 
        except FileNotFoundError:
            print("File not found.")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    # def get_course_codes(self):
    #     return json.loads(self.coursesCodes) if self.coursesCodes else []


    def get_json(self):
        return{
            'Program ID:': self.id,
            'Program Name: ': self.name,
            'Program Courses: ': self.coursesCodes
        }
       