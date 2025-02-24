from App.models import Assignee
from App import db

def create_assignee(fname, lname, email):
    new_assignee = Assignee(fname=fname, lname=lname, email=email)
    db.session.add(new_assignee)
    db.session.commit()
    return new_assignee

def get_assignee_by_id(assignee_id):
    return Assignee.query.get(assignee_id)

def get_assignee_by_fname(fname):
    return Assignee.query.filter_by(fname=fname).all()

def get_assignee_by_lname(lname):
    return Assignee.query.filter_by(lname=lname).all()

def get_assignee_by_email(email):
    return Assignee.query.filter_by(email=email).all()

def get_all_assignees():
    return Assignee.query.all()

def get_all_assignees_json():
    assignees = Assignee.query.all()
    if not assignees:
        return []
    assignees = [assignee.get_json() for assignee in assignees]
    return assignees    

def update_assignee(id, fname, lname, email):
    assignee = get_assignee_by_id(id)
    if assignee:
        assignee.fname = fname
        assignee.lname = lname
        assignee.email = email
        db.session.commit()
        return assignee
    return None
