from App.models import ProgramCourses, Program, Course
from App.controllers import (get_program_by_name, get_course_by_courseCode)
from App.database import db

def create_programCourse(programName, code, num):
    program = get_program_by_name(programName)
    if program:
        course = get_course_by_courseCode(code)
        if course:
            proCourse = ProgramCourses(program.id, code, num)
            db.session.add(proCourse)
            db.session.commit()
            #print("Course successfully added to program")
        else:
            print("Invalid course code")
    else:
        print("Invalid program name")

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

