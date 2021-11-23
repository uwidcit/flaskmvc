from flask.blueprints import Blueprint
from App.controllers import get_chatroom

chat_views = Blueprint('chat_views', __name__, template_folder="../templates")
chat_views.route("/chat", methods=["GET"])(get_chatroom)
