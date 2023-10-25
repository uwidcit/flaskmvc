from App.models import ProgramCourses, Program, Course
from App.controllers import (get_program_by_name, get_program_by_id, get_course_by_courseCode)
from App.database import db

def create_programCourse(programName, code, num):
    program = get_program_by_name(programName)
    if program:
        course = get_course_by_courseCode(code)
        if course:
            proCourse = ProgramCourses(program.id, code, num)
            db.session.add(proCourse)
            db.session.commit()
            return proCourse
        else:
            return "Invalid course code"
    else:
        return "Invalid program name"

def get_all_programCourses(programName):
    program = get_program_by_name(programName)
    return ProgramCourses.query.filter(ProgramCourses.program_id == program.id).all()

def get_allCore(programName):
    program = get_program_by_name(programName)
    core = ProgramCourses.query.filter_by(
    program_id=program.id,
    courseType=1
    ).all()
    return core if core else []

def get_allElectives(programName):
    program = get_program_by_name(programName)
    core = ProgramCourses.query.filter_by(
    program_id=program.id,
    courseType=2
    ).all()
    return core if core else []

def get_allFoun(programName):
    program = get_program_by_name(programName)
    core = ProgramCourses.query.filter_by(
    program_id=program.id,
    courseType=3
    ).all()
    return core if core else []

def convertToList(list):
    codes = []

    for a in list:
        codes.append(a.code)
    
    return codes

def programCourses_SortedbyRating(programid):
    program = get_program_by_id(programid)
    programCourses = get_all_programCourses(program.name)

    sorted_courses = {1: [], 2: [], 3: [], 4: [], 5: []}

    for p in programCourses:
        course = get_course_by_courseCode(p.code)
        sorted_courses[course.rating].append(course.courseCode)
    
    sorted_courses_list = [course for rating_courses in sorted_courses.values() for course in rating_courses]

    return sorted_courses_list

def programCourses_SortedbyHighestCredits(programid):
    program = get_program_by_id(programid)
    programCourses = get_all_programCourses(program.name)

    highTolow = []

    for p in programCourses:
        course = get_course_by_courseCode(p.code)
        if course.credits > 3:
            highTolow.insert(0,course.courseCode)
        else:
            highTolow.append(course.courseCode)

    return highTolow
