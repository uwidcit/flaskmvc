from flask import redirect, render_template, request, url_for, jsonify

from App.models import ( User, db )

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