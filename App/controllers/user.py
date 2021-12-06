from App.models import User, Admin
from App.database import db

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return users


def create_user(fname, lname, email, password):
    user = User(first_name=fname, last_name=lname, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    print(f"User created: {user.email}")
    return user


def create_users(users):
    for user in users:
        newUser = create_user(user['first_name'], user['last_name'], user['email'], user['password'], False)
        db.session.add(newUser)
    db.session.commit()


def get_user_by_fname(first_name):
    return User.query.filter_by(first_name=first_name).first()

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

    
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    

def get_all_users():
    return  User.query.all()
    
# REGISTER ADMIN USER
def create_admin(firstname, lastname, email, password):
    admin = Admin(first_name=firstname, last_name=lastname, email=email, password=password)
    db.session.add(admin)
    db.session.commit()
