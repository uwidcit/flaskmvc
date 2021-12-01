from App.controllers.user import get_all_users
from flask import Blueprint, render_template
from flask_login import login_required

chatroom_views = Blueprint('chatroom', __name__, template_folder="../templates")

@login_required
@chatroom_views.route("/chatroom", methods=["GET"])
def index():
    users = get_all_users()
    return render_template("chatroom.html", users=users)