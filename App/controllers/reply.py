from App.models.reply import Reply
from App.database import db


def create_reply(review_id, user_id, body):
    new_reply = Reply(review_id=review_id, user_id=user_id, body=body)
    db.session.add(new_reply)
    db.session.commit()
    return new_reply


def get_all_replies_by_review_id(review_id):
    return Reply.query.filter_by(review_id=review_id).all()


def get_all_replies_by_review_id_json(review_id):
    return [reply.to_json() for reply in get_all_replies_by_review_id(review_id)]


def get_reply_by_id(reply_id):
    return Reply.query.get(reply_id)


def get_reply_by_id_json(reply_id):
    return get_reply_by_id(reply_id).to_json()


def get_replies_by_user_id(user_id):
    return Reply.query.filter_by(user_id=user_id).all()


def get_replies_by_user_id_json(user_id):
    return [reply.to_json() for reply in get_replies_by_user_id(user_id)]


def update_reply(reply_id, body):
    reply = get_reply_by_id(reply_id)
    if reply:
        reply.body = body
        db.session.add(reply)
        return db.session.commit()
    return None


def delete_reply(reply_id):
    reply = get_reply_by_id(reply_id)
    if reply:
        db.session.delete(reply)
        return db.session.commit()
    return None
