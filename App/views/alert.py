from App.models.alert import Alert
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import jwt_required

alert_views = Blueprint('alert_views', __name__, template_folder='../templates')


# get alert by id
@alert_views.route('/alerts/<int:alert_id>', methods=["GET"])
@jwt_required()
def get_reply(alert_id):
    alert = get_alert_by_id(alert_id)
    return jsonify(alert.toDict())
