import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

from App.database import db, get_migrate
from App.models import User
from App.controllers.asset import *
from App.controllers.assetassignment import *
from App.controllers.assignee import *
from App.controllers.building import *
from App.controllers.floor import *
from App.controllers.provider import *
from App.controllers.room import *
from App.controllers.scanevent import *
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

    #Sample data for assets
    
    #Initialize csv 
    

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

asset_cli = AppGroup('asset', help="Asset object commands")

@asset_cli.command("create", help="creates an asset")
@click.argument("description", default="")
@click.argument("model", default="")
@click.argument("brand", default="")
@click.argument("serial_number", default="00000000")
@click.argument("room_id", default ="01")
@click.argument("last_located", default ="01")
@click.argument("assignee_id", default="01")
@click.argument("last_update", default="02/02/2002")
@click.argument("notes", default="")
@click.argument("status", default="Good Condition")

def add_asset_command(id, description, model, brand, serial_number, room_id, last_located, assignee_id,last_update, notes, status):
    asset = add_asset(id, description, model, brand, serial_number, room_id, last_located, assignee_id,last_update, notes, status)
    if asset is None:
        print('Error creating asset')
    else:
        print(f'{asset} created!')
        
        
@asset_cli.command("list_id", help="Lists assets with a ceratain id")
@click.argument("room_id", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_assets_by_room_id())
    else:
        print(get_all_assets_by_room_json())



app.cli.add_command(asset_cli) # add the group to the cli

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