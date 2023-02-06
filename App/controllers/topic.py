from App.database import db
from App.models import Topic
from sqlalchemy.exc import IntegrityError

def create_topic(name):
    topic = Topic(name)
    try:
        db.session.add(topic)
        db.session.commit()
    except IntegrityError:
        return None
    return topic

def get_topic(name):
    return Topic.query.filter_by(name=name).first()

def get_all_topics():
    return [topic.toDict() for topic in Topic.query.all()]

def set_topic_parent(name, id):
    topic = get_topic(name)
    topic.set_parent_id(id)
    db.session.add(topic)
    db.session.commit()
    return topic