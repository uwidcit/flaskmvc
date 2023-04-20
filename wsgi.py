import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, get_user_by_username)
from App.controllers.admin import ( create_competition, update_competition, delete_competition)
from App.controllers.team import  (create_team, update_team, delete_team)
from App.controllers.member import (create_member, update_member, delete_member)
from App.controllers.user import (create_user, create_admin, get_all_users, get_all_users_json)

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

@user_cli.command("create-user", help="Creates a user")
@click.argument("username", default="bob")
@click.argument("email", default="bob@bobmail.com")
@click.argument("password", default="bobpass")
def create_user_command(username, email, password):
    user = create_user(username, email, password, "user")
    print(user.to_json())

@user_cli.command("create-admin", help="Creates an admin")
@click.argument("username", default="adminbob")
@click.argument("email", default="adminbob@bobmail.com")
@click.argument("password", default="bobpass")
def create_admin_command(username, email, password):
    user = create_user(username, email, password, "admin")
    print(user.to_json())

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

@test.command("tests",help="Run tests for demonstration")
def demo_tests_command():
    admin1 = create_admin("admin", "admin@gmail.com", "adminpass")
    user1 = create_user("bob", "bob@gmail.com", "bobpass", "user")
    print(f"admin1: {admin1.to_json()}")
    print(f"user1: {user1.to_json()}")
    competition1 = create_competition_command("Comp123","07/12/2020", "14/12/2020",)


    

app.cli.add_command(test)

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


app.cli.add_command(competition_cli)



team_cli = AppGroup("team", help ="to test team commands")

@team_cli("create", help = "create a new team")
@click.argument("teamName", default="Victors")
@click.argument("score", default = "100")
def create_team_command(teamName, score):
    team = create_team(teamName, score)
    print(team.to_json())

@team_cli("update", help = "update a team")
@click.argument("id", default="1")
@click.argument("teamName", default="Victors")
@click.argument("score", default="50")
def update_team_command(id, teamName, score):
    update_team(id, teamName, score)
    print("f{id} updated")

@team_cli("delete", help = "delete a team")
@click.argument("id", default="1")
def delete_team_command(id):
    delete_team(id)
    print("f{id} deleted")

app.cli.add_command(team_cli)

member_cli = AppGroup("member", help = "to test member commands")

@member_cli("create", help = "create a member")
@click.argument("memberName", default="Joe")
def create_member_command(memberName):
    member = create_member(memberName)
    print(member.to_json())

@member_cli("update", help = "update a member")
@click.argument("id", default="1")
@click.argument("memberName", default="Jane")
def update_member_command(id, memberName):
    update_member(id, memberName)
    print("f{id} updated")

@member_cli("delete", help = "delete a member")
@click.argument("id", default="1")
def delete_member_command(id):
    delete_member(id)
    print("f{id} deleted")

app.cli.add_command(member_cli)

