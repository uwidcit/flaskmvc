from App.models import Reply
from . import db


def get_reply_by_id(id):
    print(f"Getting reply with ID: {id}")
    reply = Reply.query.filter_by(id=id).first()
    return reply


def create_new_reply(post_id):
    new_reply = Reply(originalPostId=post_id)
    print(f"Creating reply with for post: {post_id}")

    db.session.add(new_reply)
    db.session.commit()
    return new_reply
    
# TODO: Implement when more details of the reply are obtained
# def edit_reply(reply_id, text, created_date):
#     reply = get_reply_by_id(reply_id)

#     if reply:
#         reply.text = text
#         reply.created = created_date

#         print(f"Updated reply: {reply_id}")
#         db.session.add(reply)
#         db.session.commit()
#         return reply 
#     else:
#         return None


def delete_reply_by_id(id):
    reply = get_reply_by_id(id)

    if reply:
        print(f"Deleting reply with id: {id}")
        db.session.delete(reply)
        db.session.commit()
        return reply
    return None