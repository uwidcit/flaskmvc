from App.models import Assignee
from App import db

def create_assignee(fname, lname, email, room_id):
    new_assignee = Assignee(fname=fname, lname=lname, email=email, room_id=room_id)
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

def get_assignee_by_room_id(room_id):
    return Assignee.query.filter_by(room_id=room_id).all()

def get_all_assignees():
    return Assignee.query.all()

def get_all_assignees_json():
    assignees = Assignee.query.all()
    if not assignees:
        return []
    assignees = [assignee.get_json() for assignee in assignees]
    return assignees    

def update_assignee(assignee_id, fname, lname, email, room_id):
    assignee = get_assignee_by_id(assignee_id)
    if assignee:
        assignee.fname = fname
        assignee.lname = lname
        assignee.email = email
        assignee.room_id = room_id
        db.session.commit()
        return assignee
    return None
