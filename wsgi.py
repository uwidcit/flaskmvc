import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers import ( 
    create_student,
    get_all_students_json,
    get_all_students,
    get_student_by_username,
    get_student,
    update_student,
    enroll_in_programme,
    add_course_to_plan,
    remove_course_from_plan,
    view_course_plan,
    add_courses_from_file, )

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


# Define the student list command
@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == "string":
        students = get_all_students()
        for student in students:
            print(student.get_json())
    else:
        students_json = get_all_students_json()
        print(students_json)


# Define the student get-by-username command
@student_cli.command("get-by-username", help="Get a student by username")
@click.argument("username")
def get_student_by_username_command(username):
    student = get_student_by_username(username)
    if student:
        print(student.get_json())
    else:
        print(f"Student with username {username} not found.")


# Define the student get command
@student_cli.command("get", help="Get a student by ID")
@click.argument("student_id", type=int)
def get_student_command(student_id):
    student = get_student(student_id)
    if student:
        print(student.get_json())
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student update command
@student_cli.command("update", help="Update a student's username by ID")
@click.argument("student_id", type=int)
@click.argument("username")
def update_student_command(student_id, username):
    updated_student = update_student(student_id, username)
    if updated_student:
        print(f"Student updated: {updated_student.get_json()}")
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student enroll command
@student_cli.command("enroll", help="Enroll a student in a program by ID")
@click.argument("student_id", type=int)
@click.argument("programme_id")
def enroll_in_programme_command(student_id, programme_id):
    student = get_student(student_id)
    if student:
        enroll_in_programme(student, programme_id)
        print(f"Student enrolled in program with ID {programme_id}.")
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student add-course command
@student_cli.command("add-course", help="Add a course to a student's plan by ID")
@click.argument("student_id", type=int)
@click.argument("course_id")
def add_course_to_plan_command(student_id, course_id):
    student = get_student(student_id)
    if student:
        add_course_to_plan(student, course_id)
        print(f"Course with ID {course_id} added to the student's plan.")
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student remove-course command
@student_cli.command("remove-course", help="Remove a course from a student's plan by ID")
@click.argument("student_id", type=int)
@click.argument("course_id")
def remove_course_from_plan_command(student_id, course_id):
    student = get_student(student_id)
    if student:
        remove_course_from_plan(student, course_id)
        print(f"Course with ID {course_id} removed from the student's plan.")
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student view-courses command
@student_cli.command("view-courses", help="View a student's course plan by ID")
@click.argument("student_id", type=int)
def view_course_plan_command(student_id):
    student = get_student(student_id)
    if student:
        courses = view_course_plan(student)
        if courses:
            for course in courses:
                print(course)
        else:
            print("No courses found in the plan.")
    else:
        print(f"Student with ID {student_id} not found.")


# Define the student add-courses-from-file command
@student_cli.command("add-courses-from-file", help="Add courses to a student's plan from a file")
@click.argument("student_id", type=int)
@click.argument("file_path")
def add_courses_from_file_command(student_id, file_path):
    student = get_student(student_id)
    if student:
        result = add_courses_from_file(student, file_path)
        if result:
            print(result)
        else:
            print(f"Courses added from the file: {file_path}")
    else:
        print(f"Student with ID {student_id} not found.")


# Add the student command group to the app's CLI
app.cli.add_command(student_cli)

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