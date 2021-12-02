from App.controllers.reply import (create_new_reply, delete_reply_by_id, get_reply_by_id)
from App.models.reply import Reply
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import jwt_required

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
    post_id = request.json.get("post_id")

    new_reply = create_new_reply(post_id)
    return jsonify(new_reply.toDict())

# TODO: Implement when more details are obtained
# @reply_views.route("/replies/<int:reply_id>", methods=["PUT"])
# @jwt_required
# def update_reply(reply_id):
#     reply_id = request.json.get("reply_id")
#     text = request.json.get("text")
#     created_date = request.json.get("created_date")

#     reply = edit_reply(reply_id, text, created_date)

#     return jsonify(reply.toDict()) if reply else 404
    

@reply_views.route("/replies/<int:reply_id>", methods=["DELETE"])
@jwt_required()
def delete_reply(reply_id):
    result = delete_reply_by_id(reply_id)
    return jsonify(result.toDict()) if result else 404
