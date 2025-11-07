from App.models import Employer,Staff,Student
from App.database import db

def create_employer(username, password):
    newemployer = Employer(username=username, password=password)
    try: 
        db.session.add(newemployer)
        db.session.commit()
        return newemployer
    except:
        db.session.rollback()
        return None

def create_staff(username, password):
    newstaff = Staff(username=username, password=password)
    try:
        db.session.add(newstaff)
        db.session.commit()
        return newstaff
    except:
        db.session.rollback()
        return None
    
def create_student(username, password, university, degree, gpa):
    newstudent = Student(username=username, password=password, university=university, degree=degree, gpa=gpa)
    try:
        db.session.add(newstudent)
        db.session.commit()
        return newstudent
    except:
        db.session.rollback()
        return None

def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None
