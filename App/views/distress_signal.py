from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

distress_views = Blueprint('distress_views', __name__, template_folder='../templates')

@distress_views.route("/distressSignals", methods=["GET"])
@jwt_required
def get_distress_signal():
    return "."