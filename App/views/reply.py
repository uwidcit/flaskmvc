from App.controllers.reply import (create_new_reply, delete_reply_by_id, get_reply_by_id)
from App.models.reply import Reply
from App.modules.serialization_module import serialize_list
from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required, current_identity

reply_views = Blueprint('reply_views', __name__, template_folder='../templates')



# get reply by id
@reply_views.route('/replies/<int:reply_id>', methods=["GET"])
@jwt_required()
def get_reply(reply_id):
    reply = get_reply_by_id(reply_id)
    return jsonify(reply.toDict())


# get all replies
@reply_views.route("/replies", methods=["GET"])
@jwt_required()
def get_all_replies():
    replies = Reply.query.all()
    return jsonify(serialize_list(replies))


@reply_views.route("/replies", methods=["POST"])
@jwt_required()
def create_reply():
    post_id = request.json.get("replyTo")
    topic_id = request.json.get("topic_id")
    text = request.json.get("text")
    created = request.json.get("created_date")
    tag_list = request.json.get("tags")

    create_new_reply(post_id, current_identity.id, topic_id, text, created, tag_list)
    return jsonify({"message": "Created"}), 201


@reply_views.route("/replies/<int:reply_id>", methods=["DELETE"])
@jwt_required()
def delete_reply(reply_id):
    result = delete_reply_by_id(reply_id)
    return jsonify(result.toDict()) if result else 404
