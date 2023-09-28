from App.models import Program

def create_program_from_file(file_path):
    try:
        program = Program(file_path)
        return program
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def printProgramInfo(program):
    program.get_json()

