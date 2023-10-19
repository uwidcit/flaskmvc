from App.models import StudentCourseHistory
from App.controllers import (get_student_by_id, get_course_by_courseCode)
from App.database import db

def addCoursetoHistory(studentid, code):
    student  = get_student_by_id(studentid)
    if student:
        course = get_course_by_courseCode(code)
        if course:
            completed = StudentCourseHistory(studentid, code)
            db.session.add(completed)
            db.session.commit()
        else:
            print("Course doesn't exist")
    else:
        print("Student doesn't exist")
         

def getCompletedCourses(id):
    return StudentCourseHistory.query.filter_by(studentID=id).all()

def getCompletedCourseCodes(id):
    completed = getCompletedCourses(id)
    codes = []
    
    for c in completed:
        codes.append(c.code)
    
    return codes
