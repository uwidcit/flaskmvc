from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    send_from_directory,
    flash,
    redirect,
    url_for,
)
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    create_user,
    create_farmer,
    get_all_users_json,
    get_user_by_id,
    get_user_by_username,

)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


# Get all users
@user_views.route("/api/users", methods=["GET"])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)


# Identify user
@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    return jsonify(
        {
            "id": current_identity.id,
            "username": current_identity.username,
        }
    )


# Create normal user route
@user_views.route("/api/users", methods=["POST"])
def create_user_action():
    data = request.json
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "Username already exists"}), 400
    new_user = create_user(data["username"], data["password"])
    if new_user:
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "User could not be created"}), 400


# Create farmer user route
@user_views.route("/api/users/farmer", methods=["POST"])
def create_farmer_action():
    data = request.json
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "Username already exists"}), 400
    new_user = create_farmer(data["username"], data["password"])
    if new_user:
        return jsonify({"message": "Farmer created successfully"}), 201
    return jsonify({"message": "Farmer could not be created"}), 400


# Get user by id
@user_views.route("/api/users/<int:id>", methods=["GET"])
def get_user_action(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": "User not found"}), 404


# Get user by username
@user_views.route("/api/users/<string:username>", methods=["GET"])
def get_user_by_username_action(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": "User not found"}), 404
