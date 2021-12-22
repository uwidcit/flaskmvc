from App.controllers.post import (create_new_post, delete_post_by_id,
                                  edit_post, get_post_by_id,
                                  get_posts_by_topic, get_posts_by_user)
from App.models import Post
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import current_identity, jwt_required

post_views = Blueprint('post_views', __name__, template_folder='../templates')


# get post by id
@post_views.route('/posts/<int:post_id>', methods=["GET"])
@jwt_required()
def get_post(post_id):
    post = get_post_by_id(post_id)
    return jsonify(post.toDict()) if post else "Not found", 404


# get all posts
@post_views.route("/posts", methods=["GET"])
@jwt_required()
def get_all_posts():
    posts = Post.query.all()
    return jsonify(serialize_list(posts))


# get posts by user
@post_views.route("/posts/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_posts(user_id):
    posts = get_posts_by_user(user_id)
    return jsonify(serialize_list(posts))


# get posts by topic
@post_views.route("/posts/topics/<int:topic_id>", methods=["GET"])
@jwt_required()
def get_topic_posts(topic_id):
    posts = get_posts_by_topic(topic_id)
    return jsonify(serialize_list(posts))


@post_views.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    topic_id = request.json.get("topic_id")
    text = request.json.get("text")
    tag_list = request.json.get("tags")
    created_date = request.json.get("created_date")

    create_new_post(current_identity.id, topic_id,
                    text, tag_list, created_date)
    return jsonify({"message": "Created"}), 201


@post_views.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    topic_id = request.json.get("topic_id")
    text = request.json.get("text")
    tags = request.json.get("tags")
    created_date = request.json.get("created_date")

    post = edit_post(post_id, topic_id, text, tags, created_date)

    return jsonify({"message": "Updated"}) if post else 404


@post_views.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    result = delete_post_by_id(post_id)
    return jsonify({"message": f"Deleted post {post_id}"}) if result else 404
