from App.models import CoursePlanCourses
from App.database import db

def createPlanCourse(planid, code):
    course = CoursePlanCourses(planid, code)
    db.session.add(course)
    db.session.commit()

def getCourseFromCoursePlan(planid, coursecode):
    return CoursePlanCourses.query.filter_by(
        planId = planid,
        code = coursecode
    ).first()

def get_all_courses_by_planid(id):
    return CoursePlanCourses.query.filter_by(planId=id).all()

def deleteCourseFromCoursePlan(planid, coursecode):
    course = getCourseFromCoursePlan(planid, coursecode)
    if course:
        db.session.delete(course)
        db.session.commit()
        print("Course succesfully removed from course plan")
    else:
        print("Course is not in Course Plan")
