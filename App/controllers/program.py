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

def get_program(id):
    return Program.query.get(id)

def get_all_programs():
    return Program.query.all()

# def get_all_users_json():
#     program = Program.query.all()
#     if not program:
#         return []
    
#     users = [user.get_json() for user in users]
#     return users

def print_program_info(id):
    program = get_program(id)
    program.get_json()

