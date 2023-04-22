import click
import pytest
import sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate, create_db
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users)
from App.controllers.competition import ( create_competition, update_competition, delete_competition, get_competition_by_name_json)
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
def create_user_command_2(username, email, password):
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

    member1 = create_member(team1.id, admin1.id, "Timmy")
    member2 = create_member(team1.id, admin1.id,"Jimbo")
    member3 = create_member(team1.id, admin1.id,"Suzy")
    
    member4 = create_member(team2.id, admin1.id,"Sachin")
    member5 = create_member(team2.id, admin1.id,"Ceejay")
    member6 = create_member(team2.id, admin1.id,"Pappan")
          
    team1 = create_team(comp1.id, admin1.id, "Noir", "20")
    team2 = create_team(comp2.id, admin1.id, "Ceej", "13")

    print(f"team1: {team1.to_json()}")
    print(f"team2: {team2.to_json()}")

    comp1 = create_competition(admin1.id,"Comp123", "01/12/2018", "14/12/2018")
    comp2 = create_competition(admin1.id,"Comp123", "02/12/2020", "10/12/2020")
    comp3 = create_competition(admin1.id,"Comp123", "03/11/2019", "01/12/2020")

    print(f"comp1: {comp1.to_json()}")
    print(f"comp2: {comp2.to_json()}")
    print(f"comp3: {comp3.to_json()}")

@test.command("competitions", help="Search for competitions")
@click.argument("name")
def competition_search_command(name):
    competition = get_competition_by_name_json(name)
    print(competition)

app.cli.add_command(test)

competition_cli = AppGroup("competition", help = "to test competition commands")

@competition_cli.command("create", help="create a new competition")
@click.argument("admin_id", default=2)
@click.argument("compName", default="Hackathon")
@click.argument("startDate", default="07/12/2015")
@click.argument("endDate", default="14/12/2015")
def create_competition_command(admin_id, compName, startDate, endDate):
    competition = create_competition(admin_id, compName, startDate, endDate)
    print(competition.to_json())

@competition_cli.command("update", help="update a competition")
@click.argument("id", default="1")
@click.argument("admin_id", default=2)
@click.argument("compName", default="Hackar")
@click.argument("startDate", default="07/11/2015")
@click.argument("endDate", default="10/11/2015")
def update_competition_command(id,admin_id, compName, startDate, endDate):
    competition = update_competition(id,admin_id, compName, startDate, endDate)
    print(f"{id} updated")

@competition_cli.command("delete", help="delete a competition")
@click.argument("id", default="1")
def delete_competition_command(id):
    delete_competition(id)
    print(f"{id} deleted")

app.cli.add_command(competition_cli)

team_cli = AppGroup("team", help ="to test team commands")

@team_cli.command("create", help="create a new team")
@click.argument("comp_id", default="1")
@click.argument("admin_id", default="2")
@click.argument("teamName", default="Victors")
@click.argument("score", default="100")
def create_team_command(comp_id, admin_id,teamName, score):
    team = create_team(comp_id, admin_id, teamName, score)
    print(team.to_json())

@team_cli.command("update", help="update a team")
@click.argument("id", default="3")
@click.argument("teamName", default="Victors")
@click.argument("score", default="50")
def update_team_command(id,teamName, score):
    update_team(id, teamName, score)
    print(f"{id} updated")

@team_cli.command("delete", help="delete a team")
@click.argument("id", default="3")
def delete_team_command(id):
    delete_team(id)
    print(f"{id} deleted")

app.cli.add_command(team_cli)

member_cli = AppGroup("member", help = "to test member commands")

@member_cli.command("create", help="create a member")
@click.argument("teamId", default="1")
@click.argument("adminId", default="2")
@click.argument("memberName", default="Joe")
def create_member_command(teamId, adminId, memberName):
    member = create_member(teamId, adminId, memberName)
    print(member.to_json())

@member_cli.command("update", help="update a member")
@click.argument("id", default="3")
@click.argument("teamId", default="1")
@click.argument("adminId", default="2")
@click.argument("memberName", default="Jane")
def update_member_command(id, memberName):
    update_member(id,memberName)
    print(f"{id} updated")

@member_cli.command("delete", help="delete a member")
@click.argument("id", default="1")
def delete_member_command(id):
    delete_member(id)
    print(f"{id} deleted")

app.cli.add_command(member_cli)

