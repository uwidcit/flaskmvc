from flask import Blueprint
from App.controllers.auth_controller import login

auth_bp = Blueprint("auth", __name__, template_folder='../templates')
auth_bp.route("/login", methods=["GET", "POST"])(login)