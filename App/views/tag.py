from App.controllers.tag import (create_new_tag, delete_tag_by_id, edit_tag,
                                 get_tag_by_id)
from App.models.tag import Tag
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import jwt_required

tag_views = Blueprint('tag_views', __name__, template_folder='../templates')



# get tag by id
@tag_views.route('/tags/<int:tag_id>', methods=["GET"])
@jwt_required()
def get_tag(tag_id):
    tag = get_tag_by_id(tag_id)
    return jsonify(tag.toDict())


# get all tags
@tag_views.route("/tags", methods=["GET"])
@jwt_required()
def get_all_tags():
    tags = Tag.query.all()
    return jsonify(serialize_list(tags))


@tag_views.route("/tags", methods=["POST"])
@jwt_required()
def create_tag():
    text = request.json.get("text")
    created_date = request.json.get("created_date")

    new_tag = create_new_tag(text, created_date)
    return jsonify(new_tag.toDict())


@tag_views.route("/tags/<int:tag_id>", methods=["PUT"])
@jwt_required()
def update_tag(tag_id):
    text = request.json.get("text")

    tag = edit_tag(tag_id, text)

    return jsonify(tag.toDict()) if tag else 404
    

@tag_views.route("/tags/<int:tag_id>", methods=["DELETE"])
@jwt_required()
def delete_tag(tag_id):
    result = delete_tag_by_id(tag_id)
    return jsonify(result.toDict()) if result else 404
