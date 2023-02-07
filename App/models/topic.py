from App.database import db
from sqlalchemy import ForeignKey

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    parent_topic_id = db.Column(db.Integer, ForeignKey("topic.id"), nullable=True)
    parent_topic = db.relationship("Topic", backref="subtopics", remote_side=id)
    researcher_tags = db.relationship("ResearcherTag", backref="topic", lazy=True, cascade="all, delete-orphan")
    pub_tags = db.relationship("PublicationTag", backref="topic", lazy=True, cascade="all, delete-orphan")
    sub_records = db.relationship("TopicSubRecord", backref="topic", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name):
        self.name = name

    def set_parent_id(self, id):
        self.parent_topic_id = id

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subtopics': self.subtopics,
            'parent_topic_id': self.parent_topic_id
        }