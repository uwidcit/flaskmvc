import json
from App.database import db 

class OfferedCourses:
    offered = db.Column(db.String(1000))

    def __init__(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.offered = json.dumps([course_code.strip() for course_code in lines])
        
        except FileNotFoundError:
            print("File not found.")

        except Exception as e:
            print(f"An error occurred: {e}")
    
    def toString(self):
        return json.loads(self.offered) if self.offered else []
