from App.models import Program
from App.database import db

def create_program(name, core, elective, foun):
    newProgram = Program(name, core, elective, foun)
    db.session.add(newProgram)
    print("Program successfully created")
    db.session.commit()
    return newProgram
    
    

def get_program_by_name(programName):
    return Program.query.filter_by(name=programName).first()

def get_program_by_id(programId):
    return Program.query.filter_by(id=programId).first()

def get_level1_credits(programName):
    program = get_program_by_name(programName)
    return program.level1_credits if program else 0

def get_level1_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_level1_courses()
    return courses if program else []

def get_core_credits(programName):
    program = get_program_by_name(programName)
    return program.core_credits if program else 0

def get_core_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_core_courses()
    return courses if program else []

def get_elective_credits(programName):
    program = get_program_by_name(programName)
    return program.elective_credits if program else 0

def get_elective_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_elective_courses()
    return courses if program else []

def get_foun_credits(programName):
    program = get_program_by_name(programName)
    return program.foun_credits if program else 0

def get_foun_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_foun_courses()
    return courses if program else []

def get_all_courses(programName):
    core_courses = get_core_courses(programName)
    elective_courses = get_elective_courses(programName)
    foun_courses = get_foun_courses(programName)

    all = core_courses + elective_courses + foun_courses
    return all



