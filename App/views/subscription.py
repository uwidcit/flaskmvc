from App.controllers.subscription import (create_new_subscription, delete_subscription_by_id, edit_subscription,
                                 get_subscription_by_id)
from App.models.subscription import Subscription
from App.modules.serialization_module import serialize_list
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt import jwt_required

subscription_views = Blueprint('subscription_views', __name__, template_folder='../templates')



# get subscription by id
@subscription_views.route('/subscriptions/<int:subscription_id>', methods=["GET"])
def get_subscription(subscription_id):
    subscription = get_subscription_by_id(subscription_id)
    return jsonify(subscription.toDict())


# get all subscriptions
@subscription_views.route("/subscriptions", methods=["GET"])
@jwt_required
def get_all_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify(serialize_list(subscriptions))


@subscription_views.route("/subscriptions", methods=["POST"])
@jwt_required
def create_subscription():
    user_id = request.json.get("user_id")
    topic_id = request.json.get("topic_id")
    status = request.json.get("status")

    new_subscription = create_new_subscription(user_id, topic_id, status)
    return jsonify(new_subscription.toDict())


@subscription_views.route("/subscriptions/<int:subscription_id>", methods=["PUT"])
@jwt_required
def update_subscription(subscription_id):
    status = request.json.get("status")
    subscription = edit_subscription(subscription_id, status)

    return jsonify(subscription.toDict()) if subscription else 404
    

@subscription_views.route("/subscriptions/<int:subscription_id>", methods=["DELETE"])
@jwt_required
def delete_subscription(subscription_id):
    result = delete_subscription_by_id(subscription_id)
    return jsonify(result.toDict()) if result else 404
