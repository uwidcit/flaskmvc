import datetime
from App.controllers.postTag import create_new_post_tag, create_post_tags
from App.controllers.tag import create_new_tag, get_tag_by_text

from App.controllers.user import get_user_by_id
from App.models import Post
from App.models.postTag import PostTag

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


def create_new_post(user_id, topic_id, text, tag_list, created_date):
    new_post = Post(userId=user_id, topicId=topic_id, text=text, created=parse_utc_date(created_date))

    db.session.add(new_post)
    db.session.commit()

    add_tags_to_post(new_post, tag_list)

    print(f"{user_id} has created a new post to topic {topic_id}")
    return new_post
    

def edit_post(post_id, topic_id, text, tag_list, created_date):
    post = get_post_by_id(post_id)

    if post:
        post.text = text
        post.topic_id = topic_id
        post.created = parse_utc_date(created_date)

        add_tags_to_post(post, tag_list)

        print(f"Updated post: {post_id} by user: {post.userId}")
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


def parse_utc_date(date_string):
    return datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")


def add_tags_to_post(post, tag_list):
    post_tags = create_post_tags(post, tag_list)
    print(f"{len(post_tags)} tags added to post: {post.id}")


