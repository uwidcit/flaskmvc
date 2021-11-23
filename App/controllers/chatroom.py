from flask import render_template
from flask_login import login_required

from App.controllers.user import get_all_users

@login_required
def get_chatroom():
    users = get_all_users()
    return render_template("chatroom.html", users=users)