![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.command("create_employer", help="Creates an employer")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_employer_command(username, password):
    create_employer(username, password)
    print(f'employer : {username} created!')

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask user create_employer bob bobpass


@user_cli.command("create_staff", help="Creates a staff")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_staff_command(username, password):
    create_staff(username, password)
    print(f'staff : {username} created!')
```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask user create_staff tom tompass

@user_cli.command("create_student", help="Creates a student")
@click.argument("username", default="ben")
@click.argument("password", default="benpass")
@click.argument("university", default="UWI")
@click.argument("degree", nargs=-1)
@click.argument("gpa", default=3.5)
def create_student_command(username, password, university, degree, gpa):
    create_student(username, password, university, degree, gpa)
    print(f'student : {username} created!')

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask user create_student tim timpass UWI Computer Science 3.5


@app.cli.command("create-internship", help="Create an internship for an employer")
def create_internship():
    username = input("Enter your username: ")

    user = Employer.query.filter_by(username=username).first()
    if not user:
        print(f"User with username '{username}' not found.")
        return

    internship_input = input("Enter the title and description of the internship (separated by a comma): ")
    title, description = [item.strip() for item in internship_input.split(",", 1)]
    if not title or not description:
        print("Both title and description are required.")
        return
    new_internship = Internship(title=title, description=description, employer_id=user.id)
    db.session.add(new_internship)
    db.session.commit()
    print(f" Internship '{title}' created for employer '{username}'.")

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask create-internship


@app.cli.command("add-student", help="Lets a staff add a student to a shortlist")
def add_student():
    staff_username = input("Enter your staff username: ")
    staff = Staff.query.filter_by(username=staff_username).first()
    if not staff:
        print(f"Staff with username '{staff_username}' not found.")
        return

    internships = Internship.query.all()
    if not internships:
        print("No internships found.")
    else:
        print("Available Internships:")
        for internship in internships:
            print(f"ID: {internship.internship_id}, Title: {internship.title}")

    students = Student.query.all()
    if not students:
        print("No students found.")
    else:
        print("\nAvailable Students:")
        for student in students:
            print(f"Username: {student.username}, University: {student.university}, Degree: {student.degree}, GPA: {student.gpa}")

    internship_title = input("\nEnter the title of the internship to shortlist a student for: ")
    internship = Internship.query.filter_by(title=internship_title).first()
    if not internship:
        print(f"Internship with title '{internship_title}' not found.")
        return
    
    student_username = input("Enter the student's username to add to the shortlist: ")
    student = Student.query.filter_by(username=student_username).first()
    if not student:
        print(f"Student with username '{student_username}' not found.")
        return

    shortlist_entry = Shortlist(
        internship_id=internship.internship_id,
        staff_id=staff.id,
        student_id=student.id,
        status="pending"
    )
    db.session.add(shortlist_entry)
    db.session.commit()
    print(f"Student '{student_username}' added to the shortlist for internship '{internship_title}' by staff '{staff_username}' with status 'pending'.")

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask add-student


@app.cli.command("set-status", help="Lets an employer set the status of a student in a shortlist")
def set_status():
  
    employer_username = input("Enter your employer username: ")
    employer = Employer.query.filter_by(username=employer_username).first()
    if not employer:
        print(f"Employer with username '{employer_username}' not found.")
        return

    internships = Internship.query.filter_by(employer_id=employer.id).all()
    if not internships:
        print("No internships found for this employer.")
        return
    print("Available Internships:")
    for internship in internships:
        print(f"ID: {internship.internship_id}, Title: {internship.title}")

    internship_id = input("\nEnter the ID of the internship to manage its shortlist: ")
    internship = Internship.query.get(internship_id)
    if not internship or internship.employer_id != employer.id:
        print(f"Internship with ID '{internship_id}' not found for this employer.")
        return

    shortlist_entries = Shortlist.query.filter_by(internship_id=internship_id).all()
    if not shortlist_entries:
        print(f"No students in the shortlist for internship '{internship.title}'.")
        return

    print("\nShortlist Entries:")
    for entry in shortlist_entries:
        student = Student.query.get(entry.student_id)
        if student:
            print(f"Shortlist ID: {entry.shortlist_id}, "
                  f"Student ID: {student.id}, "
                  f"Username: {student.username}, "
                  f"University: {student.university}, "
                  f"Degree: {student.degree}, "
                  f"GPA: {student.gpa}, "
                  f"Status: {entry.status}")
        else:
            print(f"Shortlist ID: {entry.shortlist_id}, Student not found, Status: {entry.status}")

    student_id_input = input("\nEnter the student's ID to update status: ")
    try:
        student_id = int(student_id_input)
    except ValueError:
        print("Invalid ID. Must be an integer.")
        return

    student = Student.query.get(student_id)
    if not student:
        print(f"Student with ID '{student_id}' not found.")
        return

    shortlist_entry = Shortlist.query.filter_by(internship_id=internship_id, student_id=student.id).first()
    if not shortlist_entry:
        print(f"Shortlist entry for student ID '{student_id}' not found in this internship.")
        return

    new_status = input("Enter the new status (accept/reject): ").lower()
    if new_status not in ["accept", "reject"]:
        print("Invalid status. Please enter 'accept' or 'reject'.")
        return

    shortlist_entry.status = new_status
    db.session.commit()
    print(f"Status of student '{student.username}' (ID: {student.id}) for internship '{internship.title}' updated to '{new_status}'.")

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask set-status


@app.cli.command("view-shortlists", help="Lets students view their shortlists and statuses")
def view_shortlists():
    student_username = input("Enter your student username: ")
    student = Student.query.filter_by(username=student_username).first()
    if not student:
        print(f"Student with username '{student_username}' not found.")
        return

    shortlist_entries = Shortlist.query.filter_by(student_id=student.id).all()
    if not shortlist_entries:
        print("No shortlist entries found for this student.")
        return

    print(f"\nShortlist Entries for {student.username}:")
    for entry in shortlist_entries:
        internship = Internship.query.get(entry.internship_id)
        if internship:
            print(f"Internship Title: {internship.title}, Internship Description: {internship.description}, Status: {entry.status}")
        else:
            print(f"Internship not found for Shortlist ID: {entry.shortlist_id}, Status: {entry.status}")


```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash

$ flask view-shortlists



# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
