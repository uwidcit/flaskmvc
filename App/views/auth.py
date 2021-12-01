from App.controllers.auth import login_user, validate_user_credentials
from flask import Blueprint, flash, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect

auth_views = Blueprint("auth", __name__, template_folder='../templates')


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = validate_user_credentials(email, password)
        if user == None:
            # if user doesn't exist or password is wrong, reload the page
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember)
        return redirect(url_for('chat_views.index'))


@auth_views.route("/logout", methods=["GET"])
def logout():
    logout()
    return redirect(url_for("auth.login"))