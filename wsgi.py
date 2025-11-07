import click, pytest, sys
from flask.cli import with_appcontext, AppGroup
from App.database import create_db, db, get_migrate
from App.models import (User, Employer, Staff, Student, Shortlist, Internship, internship)
from App.main import create_app
from App.controllers import ( 
    
    create_employer,
    create_staff,
    create_student,
    get_all_users_json,
    get_all_users, initialize 
)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()
    mally = Employer(username='mally', password='mallypass')
    nicki = Employer(username='nicki', password='nickipass')
    cardi = Employer(username='cardi', password='cardipass')
    drake = Staff(username='drake', password='drakepass')
    wayne = Staff(username='wayne', password='waynepass')
    kai = Staff(username='kai', password='kaipass')
    ben = Student(username='ben', password='benpass', university='UWI', degree='Computer Science', gpa=3.5)
    angela = Student(username='angela', password='angelapass', university='UTT', degree='Finance', gpa=3.8)
    bella = Student(username='bella', password='bellapass', university='UWI', degree='Finance', gpa=3.6)
    db.session.add_all([mally, nicki, cardi, drake, wayne, kai, ben, angela, bella])
    db.session.commit()
    print('database intialized')


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

    new_status = input("Enter the new status (accepted/rejected): ").lower()
    if new_status not in ["accepted", "rejected"]:
        print("Invalid status. Please enter 'accepted' or 'rejected'.")
        return

    shortlist_entry.status = new_status
    db.session.commit()
    print(f"Status of student '{student.username}' (ID: {student.id}) for internship '{internship.title}' updated to '{new_status}'.")

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
            
#"""User Commands"""

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create_employer", help="Creates an employer")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_employer_command(username, password):
    create_employer(username, password)
    print(f'employer : {username} created!')


@user_cli.command("create_staff", help="Creates a staff")
@click.argument("username", default="bob")
@click.argument("password", default="bobpass")
def create_staff_command(username, password):
    create_staff(username, password)
    print(f'staff : {username} created!')


@user_cli.command("create_student", help="Creates a student")
@click.argument("username", default="ben")
@click.argument("password", default="benpass")
@click.argument("university", default="UWI")
@click.argument("degree", nargs=-1)
@click.argument("gpa", default=3.5)
def create_student_command(username, password, university, degree, gpa):
    create_student(username, password, university, degree, gpa)
    print(f'student : {username} created!')

# this command will be : flask user create_student ben benpass UWI "Computer Science" 3.5

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