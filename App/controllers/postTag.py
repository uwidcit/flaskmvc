from App.controllers.tag import create_new_tag, get_tag_by_text
from App.models.postTag import PostTag
from . import db


def create_new_post_tag(tag_id, post_id):
    postTag = PostTag(tagId=tag_id, postId=post_id)

    db.session.add(postTag)
    db.session.commit()

    return postTag


def create_post_tags(post, tag_list):
    post_tags = []

    for tag_text in tag_list:
        if tag_text:
            # Lookup the tag
            tag = get_tag_by_text(tag_text)

            # Tag !exists => Create new tag first
            if tag is None:
                tag = create_new_tag(tag_text)
            
            if get_post_tag(post.id, tag.id) is None:
                post_tags.append(PostTag(tag.id, post.id))
            
    # Commit all postTags to the DB
    db.session.add_all(post_tags)
    db.session.commit()
    return post_tags


def get_post_tag(post_id, tag_id):
    postTag = PostTag.query.filter_by(postId=post_id, tagId=tag_id).first()
    return postTag