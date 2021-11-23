from flask import Blueprint
from App.controllers.auth import login, logout

auth_bp = Blueprint("auth", __name__, template_folder='../templates')
auth_bp.route("/login", methods=["GET", "POST"])(login)
auth_bp.route("/logout", methods=["GET"])(logout)
