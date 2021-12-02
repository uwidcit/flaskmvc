from App.controllers.user import get_user_by_id
from App.models import Post
from . import db



def get_post_by_id(id):
    print(f"Getting post with ID: {id}")
    post = Post.query.filter_by(id=id).first()
    return post


def get_user_posts(user_id):
    user = get_user_by_id(user_id)

    if user:
        return user.posts
    else:
        raise Exception("User not found")


def create_new_post(user_id, topic_id, text, created_date):
    new_post = Post(user_id=user_id, topic_id=topic_id, text=text, created=created_date)
    print(f"{user_id} has created a new post to topic {topic_id}")

    db.session.add(new_post)
    db.session.commit()
    return new_post
    

def edit_post(post_id, topic_id, text, created_date):
    post = get_post_by_id(post_id)

    if post:
        post.text = text
        post.topic_id = topic_id
        post.created = created_date

        print(f"Updated post: {post_id} by user: {post.user_id}")
        db.session.add(post)
        db.session.commit()
        return post 
    else:
        return None

def delete_post_by_id(id):
    post = get_post_by_id(id)

    if post:
        print(f"Deleting post with id: {id}")
        db.session.delete(post)
        db.session.commit()
        return post
    return None