from App.database import db 
from App.models.member import Member
from datetime import datetime, timedelta

def create_member(teamId, adminId, name):
    member = Member(teamId = teamId, adminId = adminId, name = name)
    db.session.add(member)
    db.session.commit()
    return member

def get_member(id):
    return Member.query.get(id)
	
def get_all_members():
    return Member.query.all()
		
def update_member(id, name):
    member = get_member(id)
    if member:
        if name:
            member.name = name
        db.session.add(member)
        db.session.commit()
        return member
    return None

def delete_member(id):
    member = get_member(id)
    if member:
        db.session.delete(member)
        db.session.commit()
        return True
    return False

def get_member_by_id_json(id):
    return get_member(id).to_json()
