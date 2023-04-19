from App.database import db 
from App.models.member import Member

def create_member(memberName):
    member = Member(memberName)
    db.session.add(member)
    db.session.commit()
    return member

def get_member(memberId):
    return Member.query.get(memberId)
	
def get_all_members():
    return Member.query.all()
		
def update_member(memberId, memberName):
    member = get_member(memberId)
    if member: 
        member.memberName = memberName
        db.session.add(member)
        db.session.commit()
        return member
    return None

def delete_member(memberId):
    member = get_member(memberId)
    if member:
        db.session.delete(member)
        db.session.commit()
        return True
    return False

def get_member_by_id_json(memberId):
    return get_member(memberId).to_json()
