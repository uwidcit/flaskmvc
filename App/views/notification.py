from flask import Blueprint
from flask.json import jsonify
from flask_jwt import jwt_required

notification_views = Blueprint('notification_views', __name__, template_folder='../templates')

@notification_views.route("/notifications", methods=["GET"])
@jwt_required()
def get_all_notifications():
    return jsonify(".")


@notification_views.route("/notifications", methods=["POST"])
@jwt_required()
def create_notification():
    return jsonify(".")