from App.models import Program
from App.database import db

def create_program(file_path):
    try:
        newProgram = Program(file_path)
        db.session.add(newProgram)
        db.session.commit()
        return newProgram
    
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_program_by_name(programName):
    return Program.query.filter_by(name=programName).first()

def get_level1_credits(programName):
    program = get_program_by_name(programName)
    return program.level1_credits if program else 0

def get_level1_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_level1_courses
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
    courses = program.str_elective_courses
    return courses if program else []

def get_foun_credits(programName):
    program = get_program_by_name(programName)
    return program.foun_credits if program else 0

def get_foun_courses(programName):
    program = get_program_by_name(programName)
    courses = program.str_foun_courses
    return courses if program else []



