from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, create_access_token
from sqlalchemy.exc import IntegrityError

from.index import index_views
from .login import login_page, login_views
from .all_workouts import workout_page, all_workouts_views
from App.models.user import User
from App.models import db

from App.controllers import (
    login
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

def login_user(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    token = create_access_token(identity=user)
    return token
  return None

'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    # implement login
    data = request.form
    token = login_user(data['username'], data['password'])
    print(token)
    response = None
    if token:
        flash('Logged in successfully.')  # send message to next page
        response = redirect(url_for('all_workouts_views.workout_page'))  # redirect to main page if login successful
        set_access_cookies(response, token)
    else:
        flash('Invalid username or password')  # send message to next page
        response = redirect(url_for('login_views.login_page'))
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return render_template('login.html')

'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route("/signup", methods=['GET'])
def signup_page():
    return render_template("signup.html")

@auth_views.route("/signup", methods=['POST'])
def signup_action():
  response = None
  try:
    username = request.form['username']
    password = request.form['password']
    
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    response = redirect(url_for('login_views.login_page'))
    token = create_access_token(identity=user)
    set_access_cookies(response, token)
  except IntegrityError:
    flash('Username already exists')
    response = redirect(url_for('auth_views.signup_page'))
  flash('Account created')
  return response