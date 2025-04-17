from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies


from.index import index_views

from App.controllers import (
    login
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




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
    

@auth_views.route('/login', methods=['GET', 'POST'])
def login_action():
    if request.method == 'GET':
        return render_template('index.html')
    
    # Handle POST: get username and password from the login form
    username = request.form.get('username')
    password = request.form.get('password')
    
    token = login(username, password)  # This should return a JWT if authentication is successful
    if not token:
        flash('Invalid credentials', 'error')
        return redirect(url_for('auth_views.login_action'))
    
    # Create response
    response = redirect(url_for('home_views.home_page'))
    
    # Set JWT in both cookie and header
    set_access_cookies(response, token)
    response.headers['Authorization'] = f'Bearer {token}'
    
    # Set cookie max age and other options
    response.set_cookie(
        'access_token',
        token,
        httponly=True,
        secure=True,  # Required for SameSite=None
        samesite='Lax',  # More secure than 'None'
        max_age=3600,  # 1 hour
        path='/'  # Ensure cookie is available for all paths
    )
    
    flash('Login successful!', 'success')
    return response

@auth_views.route('/signup', methods=['GET'])
def signup_action():
    return render_template('signup.html')  # Make sure you have this template

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(request.referrer) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response


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