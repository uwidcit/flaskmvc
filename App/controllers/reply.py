from App.controllers.post import add_tags_to_post, get_post_by_id, parse_utc_date
from App.models import Reply
from . import db


def get_reply_by_id(id):
    print(f"Getting reply with ID: {id}")
    reply = Reply.query.filter_by(id=id).first()
    return reply


def create_new_reply(post_id, user_id, topic_id, text, created, tag_list):
    original_post = get_post_by_id(post_id)

    if original_post:
        print(f"Creating reply for post: {post_id}")
        
        new_reply = Reply(post_id, user_id, topic_id, text, parse_utc_date(created))
        
        db.session.add(new_reply)
        db.session.commit()

        add_tags_to_post(new_reply, tag_list)
        return new_reply
    return None
    

def delete_reply_by_id(id):
    reply = get_reply_by_id(id)

    if reply:
        print(f"Deleting reply with id: {id}")
        db.session.delete(reply)
        db.session.commit()
        return reply
    return None