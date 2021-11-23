from flask import Blueprint, redirect, render_template, request, jsonify, send_from_directory, url_for, flash

from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from App.models.user import db
from App.controllers import ( get_all_users_json, get_all_users, register, display_all_users )

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users')
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users')
def static_user_page():
  return send_from_directory('static', 'static-user.html')

# REGISTRATION NORMAL USER

@user_views.route('/register', methods=['GET','POST'])
def get_user_reg_page():
    if request.method == 'POST':
        try:
            RegisterUser = register()
        except IntegrityError:
            db.session.rollback()
            return jsonify('Something went wrong. User NOT Registered')
        return jsonify('User Registered')
        
    return render_template('register.html')  


