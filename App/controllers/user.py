from flask import redirect, render_template, request, url_for, jsonify

from App.models import ( User, db )
from App.models import user

def create_user(firstname, lastname, uwi_id, email, gender, dob):
    # newuser = use()
    return 'new user'

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return users

def create_user(fname, lname, email, password):
    user = User(first_name=fname, last_name=lname, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

def create_users(users):
    for user in users:
        newuser = User(first_name=user['first_name'], last_name=user['last_name'], email=user['email'])
        newuser.set_password(user['password'])
        db.session.add(newuser)
    db.session.commit()

def get_user_by_fname(first_name):
    return User.query.filter_by(first_name=first_name).first()

def get_all_users():
    return  User.query.all()

# REGISTER A NORMAL USER
def register():
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        publicUser = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(publicUser)
        db.session.commit()
    
# REGISTER ADMIN USER
def register_admin(firstname, lastname, email, password):
        adminUser = User(first_name=firstname, last_name=lastname, email=email,password=password)
        adminUser.set_password(password)
        db.session.add(adminUser)
        db.session.commit()
        print("Administrator Successfully Created!!!")
        return adminUser