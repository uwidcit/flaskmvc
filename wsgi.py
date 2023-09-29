import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    create_program,
    get_program,
    create_course,
    print_program_info
    )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)


'''
Program Commands
'''

program = AppGroup('program', help = 'Program object commands')

@program.command('create', help='Create a new program')
@click.argument('file_path')
def create_program_command(file_path):  
    with open(file_path, 'r') as file:
        course_codes = [code.strip() for code in file.readlines()[1:]]
        print('Course codes:', course_codes)  # Print the course codes
        newprogram = create_program(file_path)
        print(f'Program created with ID {newprogram.id} and name "{newprogram.name}" and courses of this program are {newprogram.get_course_codes()}')

# @program.command('display', help='Display program information')
# @click.argument('program_id', type=int)
# def display_program_command(program_id):
#     print_program_info(program_id)


@program.command('getProgram', help='Get program by name')
@click.argument('id', type=int)
def get_Program_command(id):
    program = get_program(id)
    if program:
        r = program.get_json()
        print(r)
    else:
        print(f'Program with ID "{id}" not found.')

app.cli.add_command(program)


'''
Course Commands
'''

course = AppGroup('course', help = 'Program object commands')

@course.command('create', help='Create a new course')
@click.argument('file_path')
def create_course_command(file_path):  
    with open(file_path, 'r') as file:
        newcourse = create_course(file_path)
        print(f'Course created with course code "{newcourse.courseCode}", name "{newcourse.courseName}", credits "{newcourse.credits}", ratings "{newcourse.rating}" and prerequites "{newcourse.prerequisites}"')


app.cli.add_command(course)