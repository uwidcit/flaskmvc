from App.models import Course
from App.database import db
import json

def create_course(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i in range(0, len(lines), 6):
                course = Course()
                course.courseCode = lines[i].strip()
                course.courseName = lines[i + 1].strip()
                course.credits = int(lines[i + 2].strip())
                course.rating = int(lines[i + 3].strip())
                course.prerequisites = json.dumps(lines[i + 4].strip().split(','))
                db.session.add(course)

        db.session.commit()

    except FileNotFoundError:
        print("File not found.")
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def get_course_by_courseCode(code):
    return Course.query.filter_by(courseCode=code).first()

def get_prerequisites(code):
    course = get_course_by_courseCode(code)
    return course.prerequisites if course else None

def get_credits(code):
    course = get_course_by_courseCode(code)
    return course.credits if course else 0

def get_ratings(code):
    course = get_course_by_courseCode(code)
    return course.rating if course else 0

