from flask import Blueprint

from App.controllers.auth import login, logout

auth_views = Blueprint("auth_views", __name__, template_folder='../templates')

auth_views.route("/login", methods=["GET", "POST"])(login)
auth_views.route("/logout", methods=["GET"])(logout)
