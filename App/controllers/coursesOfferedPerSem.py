from App.models import CoursesOfferedPerSem
from App.controllers import get_course_by_courseCode
from App.database import db

def addSemesterCourses(courseCode):
    course = get_course_by_courseCode(courseCode)
    if course:
        semCourses = CoursesOfferedPerSem(courseCode)
        db.session.add(semCourses)
        db.session.commit()
        return semCourses
    else:
        print("Course not found")

def delete_all_records():
    try:
        db.session.query(CoursesOfferedPerSem).delete()
        db.session.commit()
        print("All records deleted successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {str(e)}")

def isCourseOffered(courseCode):
    course = CoursesOfferedPerSem.query.filter_by(code=courseCode).first()
    return True if course else False

def get_all_courses():
    return CoursesOfferedPerSem.query.all()

def get_all_OfferedCodes():
    offered = get_all_courses()
    offeredcodes=[]

    for c in offered:
        offeredcodes.append(c.code)
    
    return offeredcodes
