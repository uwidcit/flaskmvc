from App.models import Course
from App.database import db

def create_course(file_path):
    try:
        newCourse = Course(file_path)
        db.session.add(newCourse)
        db.session.commit()
        return newCourse
    
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

