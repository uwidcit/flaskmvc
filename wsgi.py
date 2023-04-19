import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_user_by_username)
from App.controllers.admin import ( create_competition, update_competition, delete_competition)

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

# create a group, it would be the first argument of the command
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

#creates users for tests
@app.cli.command("create-users")
@click.argument("number", default=4)
def create_users_command(number):
    for i in range(1, number + 1):
        user = get_user_by_username(f"rob{i}")
        if not user:
            create_user(f"rob{i}", f"rob{i}pass")
            print(f"rob{i} created!")
        else:
            print(f"rob{i} already exists")

@app.cli.command("create-user")
@click.argument("number", default="1")
def create_user_command(number):
    user = get_user_by_username(f"bob{number}")
    if not user:
        create_user(f"bob{number}", "bobpass")
        print(f"bob{number} created!")
    else:
        print(f"bob{number} already exists")

competition_cli = AppGroup("competition", help = "to test competition commands")

@competition_cli("create", help = "create a new competition")
@click.argument("name", default="Hackathon")
@click.argument("start date", default="07/12/2015")
@click.argument("end date", default="14/12/2015")
@click.argument("team", default="Victors")
def create_competition_command(name, start_date, end_date, team):
    competition = create_competition(name, start_date, end_date, team)
    print(competition.to_json())

@competition_cli("update", help = "update a competition")
@click.argument("compCode", default="1")
@click.argument("name", default="Hackathon")
@click.argument("start date", default="07/12/2015")
@click.argument("end date", default="16/12/2015")
@click.argument("team", default = "Victors")
def update_competition_command(self, compCode, name, start_date, end_date, team):
    update_competition(self, compCode, name, start_date, end_date, team)
    print("f{compCode} updated")

@competition_cli("delete", help = "delete a competition")
@click.argument("compCode", default="1")
def delete_competition_command(self, compCode):
    delete_competition(self, compCode)
    print("f{compCode} deleted")

