import click, pytest, sys
from flask import Flask
from App.controllers.admin import addStaff, createAdmin, removeAccount
from App.controllers.student import create_student
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( 
    create_user, 
    get_all_users_json, 
    get_all_users, 
    create_program,
    get_core_courses,
    get_core_credits,
    create_course,
    get_course_by_courseCode,
    get_prerequisites,
    get_all_courses,
    getRemainingCourses,
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


# ... (previous code remains the same)

'''
Student
'''
student_cli = AppGroup("student", help="Student object commands")

# Define the student create command
@student_cli.command("create", help="Creates a student")
@click.argument("username")
@click.argument("password")
@click.argument("student_id")
@click.argument("name")
def create_student_command(username, password, student_id, name):
    create_student(username, password, student_id, name)
    print(f"Student {username} created.")

app.cli.add_command(student_cli)

'''
Admin Commands
'''

admin_cli = AppGroup("admin", help="Admin object commands")

# Define the admin create command
@admin_cli.command("create_admin", help="Creates an admin")
@click.argument("id")
@click.argument("username")
@click.argument("password")
@click.argument("name")
def create_admin_command(id, username, password, name):
  createAdmin(id, username, password, name)

@admin_cli.command("create_staff", help="Creates a staff member")
@click.argument("id")
@click.argument("username")
@click.argument("password")
@click.argument("name")
def create_staff_command(id, username, password, name):
  addStaff(id, username, password, name)
  print(f"Staff member {username} created")

@admin_cli.command("delete", help="Creates a staff member")
@click.argument("id")
def delete_user_command(id):
  removeAccount(id)

app.cli.add_command(admin_cli)

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
#################################################################

'''
Program Commands
'''

program = AppGroup('program', help = 'Program object commands')

@program.command('create', help='Create a new program')
@click.argument('file_path')
def create_program_command(file_path):  
    with open(file_path, 'r') as file:
        newprogram = create_program(file_path)
        print(f'Program created with ID {newprogram.id} and name "{newprogram.name}"')

@program.command('core', help='Get program core courses')
@click.argument('programname', type=str)
def get_CoreCourses(programname):
    courses = get_core_courses(programname)
    print(f'{courses}') if courses else print(f'error')

@program.command('corecredits', help='Get program core courses')
@click.argument('programname', type=str)
def get_CoreCredits(programname):
    credits = get_core_credits(programname)
    print(f'Total Core Credits = {credits}') if credits else print(f'error')

@program.command('allcourses', help='Get all courses')
@click.argument('programname', type=str)
def allCourses(programname):
    all = get_all_courses(programname)
    print(f'All courses are = {all}') if credits else print(f'error')


app.cli.add_command(program)
#################################################################

'''
Course Commands
'''

course = AppGroup('course', help = 'Program object commands')

@course.command('create', help='Create a new course')
@click.argument('file_path')
def create_course_command(file_path):  
    newcourse = create_course(file_path)
    print(f'Course created with course code "{newcourse.courseCode}", name "{newcourse.courseName}", credits "{newcourse.credits}", ratings "{newcourse.rating}" and prerequites "{newcourse.prerequisites}"')


@course.command('prereqs', help='Create a new course')
@click.argument('code', type=str)
def create_course_command(code):  
    prereqs = get_prerequisites(code)
    print(f'These are the prerequisites for {code}: {prereqs}') if prereqs else print(f'error')

@course.command('getcourse', help='Get a course by course code')
@click.argument('code', type=str)
def get_course(code):  
    course = get_course_by_courseCode(code)
    print(f'Course Name: {course.courseName}') if course else print(f'error')


app.cli.add_command(course)

###########################################################

'''
Course Plan Commands
'''

coursePlan = AppGroup('plan', help = 'Course Plan object commands')

@coursePlan.command('remaining', help='Get remaining program courses')
@click.argument('programname', type=str)
def remaining(programname):  
    required = get_all_courses(programname)
    completed = ['COMP1600']
    newRemaining = getRemainingCourses(completed, required)
    print(f'Remaining courses are: {newRemaining}')


app.cli.add_command(coursePlan)