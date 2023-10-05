from App.models import OfferedCourses
from App.controllers import get_course_by_courseCode
from App.database import db
import json

def addSemesterCourses(courseCode):
    course = get_course_by_courseCode(courseCode)
    if course:
        semCourses = OfferedCourses(courseCode)
        db.session.add(semCourses)
        db.session.commit()
        return course
    else:
        print("Course not found")

def removeAllCourses(semCourses):
    semCourses.offered = json.dumps([])
    return semCourses

def get_all_courses(semCourses):
    return semCourses.offeredCourses