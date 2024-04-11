from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

signup_views = Blueprint('signup_views', __name__, template_folder='../templates')

'''
Action Routes
'''    
# @signup_views.route('/signup', methods=['POST'])
# def signup_action():
#     data = request.form
#     user = create_user(data['username'], data['password'])
#     response = redirect(url_for('login_views.login_page'))
#     if not user:
#         flash('Problem Creating New Account'), 401
#     else:
#         flash('Sign Up Successful')
#     return response

'''
Page Routes
'''   
@signup_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')