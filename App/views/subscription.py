from App.controllers.subscription import (create_new_subscription,
                                          delete_subscription_by_id,
                                          get_subscription_by_id,
                                          get_subscriptions_by_user)
from App.models.subscription import Subscription
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import jwt_required

subscription_views = Blueprint('subscription_views', __name__, template_folder='../templates')


# get subscription by id
@subscription_views.route('/subscriptions/<int:subscription_id>', methods=["GET"])
@jwt_required()
def get_subscription(subscription_id):
    subscription = get_subscription_by_id(subscription_id)
    return jsonify(subscription.toDict()) if subscription else ("Not found", 404)


# get all subscriptions
@subscription_views.route("/subscriptions", methods=["GET"])
@jwt_required()
def get_all_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify(serialize_list(subscriptions))


@subscription_views.route("/subscriptions/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_subscriptions(user_id):
    subscriptions = get_subscriptions_by_user(user_id)
    return jsonify(serialize_list(subscriptions))



@subscription_views.route("/subscriptions", methods=["POST"])
@jwt_required()
def create_subscription():
    user_id = request.json.get("user_id")
    topic_id = request.json.get("topic_id")

    create_new_subscription(user_id, topic_id)
    return jsonify({"message": "created"}), 201


# TODO: Remove if unncessary
# @subscription_views.route("/subscriptions/<int:subscription_id>", methods=["PUT"])
# @jwt_required()
# def update_subscription(subscription_id):
#     status = request.json.get("status")
#     subscription = edit_subscription(subscription_id, status)

#     return jsonify(subscription.toDict()) if subscription else 404
    

@subscription_views.route("/subscriptions/<int:subscription_id>", methods=["DELETE"])
@jwt_required()
def delete_subscription(subscription_id):
    result = delete_subscription_by_id(subscription_id)
    return jsonify({"message": "Unsubscribed"}), 201 if result else ("Not found", 404)
