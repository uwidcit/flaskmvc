from App.controllers.auth import login_user, logout_user, validate_user_credentials
from flask import Blueprint, flash, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

from App.controllers import ( create_user )

auth_views = Blueprint("auth", __name__, template_folder='../templates')

@auth_views.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_views.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')  

@auth_views.route('/signup', methods=['POST'])
def signup_action():
    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    res = create_user(fname, lname, email, password)
    if (res):
        flash('User Created')
        return redirect('/')
    else:
        flash("Email Taken")
        return redirect('/signup')
        
@auth_views.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect('/')
