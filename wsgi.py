import click
from flask import Flask
from flask.cli import with_appcontext

from App.database import create_db
from App.main import app, migrate
from App.controllers import ( create_user, get_all_users_json )


@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@app.cli.command("get-users")
def get_users():
    print(get_all_users_json())