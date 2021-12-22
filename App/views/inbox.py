from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required

inbox_views = Blueprint('inbox_views', __name__, template_folder='../templates')

from App.controllers.inbox import (
    get_inbox_feed_by_id
)

# Get feed by ID
@inbox_views.route('/inbox/<int:inbox_id>', methods=["GET"])
def get_feed(postId):
    InboxFeed = get_inbox_feed_by_id(postId)
    return jsonify(InboxFeed.toDict())