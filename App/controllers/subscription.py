from . import db
from App.models import Subscription
from datetime import datetime


def get_subscription_by_id(id):
    print(f"Getting subscription with ID: {id}")
    subscription = Subscription.query.filter_by(id=id).first()
    return subscription


def create_new_subscription(user_id, topic_id, status):
    new_subscription = Subscription(user_id=user_id, topic_id=topic_id, status=status)
    print(f"Creating subscription for user: {user_id} and topic: {topic_id}")

    db.session.add(new_subscription)
    db.session.commit()
    return new_subscription
    

def edit_subscription(subscription_id, status):
    subscription = get_subscription_by_id(subscription_id)

    if subscription:
        subscription.status = status
        subscription.created = datetime.now

        print(f"Updated subscription: {subscription_id}")
        db.session.add(subscription)
        db.session.commit()
        return subscription 
    else:
        return None


def delete_subscription_by_id(id):
    subscription = get_subscription_by_id(id)

    if subscription:
        print(f"Deleting subscription with id: {id}")
        db.session.delete(subscription)
        db.session.commit()
        return subscription
    return None