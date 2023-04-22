from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
#from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from flask_jwt import current_identity, jwt_required

from flask_jwt import jwt_required, current_identity

from App.controllers import(
    create_user,
    delete_user,
    get_all_users_json,
    get_user_by_id,
    get_user_by_username,
    get_user_by_email,
    update_user,
    is_admin,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")

# Get all users
@user_views.route("/api/users", methods=["GET"])
@jwt_required()
def get_users_action():
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to view all users"}), 401
    users = get_all_users_json()
    if not users:
        return jsonify([]), 200
    return jsonify(users)

# Identify user
@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify():
    return jsonify(
        {
            "id": current_identity.id,
            "username": current_identity.username,
            "access": current_identity.access,
        }
    )

# Create normal user route
@user_views.route("/api/users", methods=["POST"])
def create_user_action():
    data = request.json
    if not data["email"] or not data["username"] or not data["password"]:
        return jsonify({"message": "Please fill out all fields"}), 400
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_user(data["username"], data["email"], data["password"], access="user")
    if new_user:
        return jsonify(new_user.to_json()), 201
    return jsonify({"message": "User could not be created"}), 400

@user_views.route("/api/users/admin", methods=["POST"])
@jwt_required()
def create_admin_action():
    data = request.json
    if not is_admin(current_identity):
        return jsonify({"message": "You are not authorized to create an admin"}), 401
    user = get_user_by_email(data["email"])
    if user:
        return jsonify({"message": "email already exists"}), 400
    user = get_user_by_username(data["username"])
    if user:
        return jsonify({"message": "username already exists"}), 400
    new_user = create_user(data["username"], data["email"], data["password"], access="admin")
    if new_user:
        return (
            jsonify(new_user.to_json()),
            201,
        )
    return jsonify({"message": "Admin could not be created"}), 400


# Get user by id
@user_views.route("/api/users/<int:id>", methods=["GET"])
def get_user_action(id):
    user = get_user_by_id(id)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"User {id} not found"}), 404

# Get user by email
@user_views.route("/api/users/email", methods=["GET"])
def get_user_by_email_action():
    data = request.json
    user = get_user_by_email(data["email"])
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"{data['email']} not found"}), 404


# Get user by username
@user_views.route("/api/users/<string:username>", methods=["GET"])
def get_user_by_username_action(username):
    user = get_user_by_username(username)
    if user:
        return jsonify(user.to_json())
    return jsonify({"message": f"{username} not found"}), 404

# Update user
@user_views.route("/api/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user_action(id):
    if not is_admin(current_identity):
        if id != current_identity.id:
            return (
                jsonify({"message": "You are not authorized to update this user"}),
                401,
            )
    data = request.json
    user = get_user_by_id(id)
    if user:
        if "username" in data:
            if get_user_by_username(data["username"]):
                return jsonify({"message": "Username already exists"}), 400
            else:
                user = update_user(id=id, username=data["username"])
        if "email" in data:
            if get_user_by_email(data["email"]):
                return jsonify({"message": "Email already exists"}), 400
            else:
                user = update_user(id=id, email=data["email"])
        if "password" in data:
            user = update_user(id=id, password=data["password"])
        return jsonify(user.to_json()), 200
    return jsonify({"message": "User not found"}), 404

#delete user  
@user_views.route("/api/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user_action(id):
    user = get_user_by_id(id)
    if user:
        delete_user(id)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# @user_views.route("/signup", methods=["GET"])
# def signup_up()
