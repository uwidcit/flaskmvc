import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import create_db, get_migrate, drop_db
from App.main import create_app
from App.controllers import ( create_researcher, get_researcher_by_email, get_all_users_json, get_all_users,
                                create_topic, set_topic_parent, get_topic, get_all_topics
)

from App.models import User, Student, Researcher

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    create_db(app)
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
researcher_cli = AppGroup('researcher', help='Researcher object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@researcher_cli.command("create", help="Creates a researcher")
@click.argument("email", default="test@mail.com")
@click.argument("password", default="testpass")
@click.argument("first_name", default="Bob")
@click.argument("middle_name", default="Rob")
@click.argument("last_name", default="Bobbert")
@click.argument("institution", default="UWI")
@click.argument("faculty", default="FST")
@click.argument("department", default="DCIT")
@click.argument("title", default="Mr.")
@click.argument("position", default="Tutor")
@click.argument("start_year", default="2019")
@click.argument("qualifications", default="B.Sc. Computer Science (UWI)\nM.Sc. Computer Science (UWI)")
@click.argument("skills", default="Android Development\nData Mining\nAlgorithm Design")
def create_researcher_command(email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, start_year, qualifications, skills):
    create_researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, start_year, qualifications, skills)
    print(f'{first_name} {last_name} created!')

# this command will be : flask user create bob bobpass

@researcher_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@researcher_cli.command("get", help="Gets a specific researcher")
@click.argument("email", default="test@mail.com")
def get_researcher_command(email):
    print(get_researcher_by_email(email).toDict())

app.cli.add_command(researcher_cli) # add the group to the cli


user_cli = AppGroup("user", help="User object commands")

@user_cli.command("create")
def create_user_command():
    user = Researcher()
    user2 = Student()
    user.set_password('test')
    user.addSubscriber(user2)
    if user:
        print("User created")
        print(user.password)

app.cli.add_command(user_cli)


topic_cli = AppGroup('topic', help='Topic object commands') 

@topic_cli.command("create", help="Creates a topic")
@click.argument("name")
def create_topic_command(name):
    topic = create_topic(name)
    print(f'{topic.name} created')

@topic_cli.command("setParent", help="Updates topic parent")
@click.argument("name")
@click.argument("id")
def set_parent_id_command(name, id):
    topic = set_topic_parent(name, id)
    print(topic.parent_topic.name)

@topic_cli.command("list", help="Lists all topics")
def list_topics():
    topics = get_all_topics()
    print(topics)

app.cli.add_command(topic_cli)

'''
Generic Commands
'''

@app.cli.command("init")
def initialize():
    create_db(app)
    print('database intialized')

@app.cli.command("drop")
def initialize():
    create_db(app)
    print('database destroyed')

@app.cli.command("run")
def initialize():
    print('hello')

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