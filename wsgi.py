import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.competition import ( 
    create_competition, 
    get_all_competitions, 
    import_competition_results, 
    get_competition_results 
)

app = create_app()
migrate = get_migrate(app)
#-------------- SIR ---------------
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

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

from App.controllers.competition import ( 
    create_competition, 
    get_all_competitions, 
    import_competition_results, 
    get_competition_results 
)
import click
#-----------------------------

#1. Create a competition
@app.cli.command("create-competition", help="Creates a new coding competition")
@click.argument("competition_name")
@click.argument("date_occurred")  # e.g., 2024-09-18
@click.argument("competition_description", required=False)
def create_competition_command(competition_name, date_occurred, competition_description=None):
    date_obj = datetime.strptime(date_occurred, '%Y-%m-%d')
    competition = create_competition(competition_name, date_obj, competition_description)
    print(f'Competition {competition.competition_Name} created!')

#2. Import competition results from file
@app.cli.command("import-results", help="Import competition results from a file")
@click.argument("competition_id")
@click.argument("file_path")
def import_competition_results_command(competition_id, file_path):
    success, imported_results = import_competition_results(competition_id, file_path)
    
    if success:
        print("Import successful, here are the imported results:")
        for result in imported_results:
            print(result.get_json())  # Print the JSON representation of each result
    else:
        print("Import failed!")

#3. List competitions
@app.cli.command("list-competitions", help="Lists all competitions")
def list_competitions_command():
    competitions = get_all_competitions()
    for competition in competitions:
        print(competition.get_json())

#4. View competition results
@app.cli.command("view-results", help="Displays result of a specific student in a competition")
@click.argument("competition_id")
@click.argument("student_name")
def view_results_command(competition_id, student_name):
    results = get_competition_results(competition_id)
    if results:
        student_result = next((result for result in results if result.student.lower() == student_name.lower()), None)
        if student_result:
            print(student_result.get_json())
        else:
            print(f'No result found for student {student_name} in competition {competition_id}')
    else:
        print(f'No results found for competition {competition_id}')

