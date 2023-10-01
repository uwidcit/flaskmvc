import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )

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
Staff Commands
'''

staff_cli = AppGroup('staff', help='Staff object commands')

@staff_cli.command("add_programme", help="Add a program")
@click.argument("program_name")
@click.argument("description")
def add_programme_command(program_name, description):
    from App.controllers.staff import StaffController  # Import the StaffController
    staff_controller = StaffController()  # Initialize the StaffController
    staff_controller.add_programme(program_name, description)  # Call the add_programme method
    print(f"Program '{program_name}' added!")

@staff_cli.command("remove_programme", help="Remove a program")
@click.argument("program_name")
def remove_programme_command(program_name):
    from App.controllers.staff import StaffController  # Import the StaffController
    staff_controller = StaffController()  # Initialize the StaffController
    staff_controller.remove_programme(program_name)  # Call the remove_programme method
    print(f"Program '{program_name}' removed!")

@staff_cli.command("add_course", help="Add a course")
@click.argument("course_code")
@click.argument("course_name")
@click.argument("credits", type=int)
def add_course_command(course_code, course_name, credits):
    from App.controllers.staff import StaffController  # Import the StaffController
    staff_controller = StaffController()  # Initialize the StaffController
    staff_controller.add_course(course_code, course_name, credits)  # Call the add_course method
    print(f"Course '{course_code}' added!")

@staff_cli.command("remove_course", help="Remove a course")
@click.argument("course_code")
def remove_course_command(course_code):
    from App.controllers.staff import StaffController  # Import the StaffController
    staff_controller = StaffController()  # Initialize the StaffController
    staff_controller.remove_course(course_code)  # Call the remove_course method
    print(f"Course '{course_code}' removed!")

app.cli.add_command(staff_cli)

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