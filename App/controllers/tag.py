from datetime import datetime
from App.models import Tag
from . import db


def get_tag_by_id(id):
    print(f"Getting tag with ID: {id}")
    tag = Tag.query.filter_by(id=id).first()
    return tag


def get_tag_by_text(text):
    print(f"Getting tag with text: {text}")
    return Tag.query.filter_by(text=text).first()


def create_new_tag(text):
    new_tag = Tag(text=text)
    print(f"Creating tag with text: {text}")

    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def edit_tag(tag_id, text):
    tag = get_tag_by_id(tag_id)

    if tag:
        tag.text = text
        tag.created = datetime.utcnow()

        print(f"Updated tag: {tag_id}")
        db.session.add(tag)
        db.session.commit()
        return tag
    else:
        return None


def delete_tag_by_id(id):
    tag = get_tag_by_id(id)

    if tag:
        print(f"Deleting tag with id: {id}")
        db.session.delete(tag)
        db.session.commit()
        return tag
    return None
