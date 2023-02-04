from App.database import db

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    parent_topic_id = db.Column(db.Integer, ForeignKey("Topic.id"), nullable=True)
    subtopics = db.relationship("Topic", backref="topic")