from flask.blueprints import Blueprint
from App.controllers.chatroom import get_chatroom

chatroom_bp = Blueprint('chatroom', __name__, template_folder="../templates")
chatroom_bp.route("/chatroom", methods=["GET"])(get_chatroom)
