from App.models import OfferedCourses
from App.database import db
import json

def addSemesterCourses(file_path):
    semCourses = OfferedCourses(file_path)
    db.sesssion.add(semCourses)
    db.session.commit()
    return semCourses

def removeAllCourses(semCourses):
    semCourses.offered = json.dumps([])
    return semCourses

def get_all_courses(semCourses):
    return semCourses.offeredCourses