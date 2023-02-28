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
    get_user_by_email,
    update_user,
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
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_user(data["username"], data["email"], data["password"])
    if new_user:
        return jsonify({"message": "User created successfully"}), 201
    return jsonify({"message": "User could not be created"}), 400


# Create farmer user route
@user_views.route("/api/users/farmer", methods=["POST"])
def create_farmer_action():
    data = request.json
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_farmer(data["username"], data["email"], data["password"])
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


# Get user by email
@user_views.route("/api/users/<string:email>", methods=["GET"])
def get_user_by_email_action(email):
    user = get_user_by_email(email)
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


# Update user
@user_views.route("/api/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_action(id):
    data = request.json
    user = get_user_by_id(id)
    if user:
        if user.id == current_identity.id:
            update_user(
                id=data["id"],
                username=data["username"],
                email=data["email"],
                password=data["password"],
                phone=data["phone"],
                address=data["address"],
                currency=data["currency"],
                units=data["units"],
                avatar=data["avatar"],
            )
            return jsonify({"message": "User updated successfully"}), 200
        return jsonify({"message": "You are not authorized to update this user"}), 403
    return jsonify({"message": "User not found"}), 404
