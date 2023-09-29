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

def get_course_by_name(name):
    return Course.query.filter_by(courseName=name).first()

def get_course_by_courseCode(code):
    return Course.query.get(courseCode=code).first()

def get_prerequisites(code):
    course = get_course_by_courseCode(code)
    if course:
        return course.prerequisites
    else: 
        return None

def get_credits(code):
    course = get_course_by_courseCode(code)
    if course:
        return course.credits
    else: 
        return None


def get_all_courses():
    return Course.query.all()