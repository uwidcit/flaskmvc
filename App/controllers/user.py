from flask import redirect, render_template, request, session, url_for

from App.models import ( User )

def create_user(firstname, lastname, uwi_id, email, gender, dob):
    # newuser = use()
    return 'new user'