from App.models import Researcher, User
from App.database import db

def create_researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, 
                    start_year, qualifications, skills):
    newresearcher = Researcher(email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, start_year, qualifications, skills)
    db.session.add(newresearcher)
    db.session.commit()
    return newresearcher

def get_researcher_by_email(email):
    return Researcher.query.filter_by(email=email).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    
    for user in users:
        print(user)
    users = [user.toDict() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None
    