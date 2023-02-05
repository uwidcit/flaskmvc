from App.database import db
from sqlalchemy import ForeignKey

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    parent_topic_id = db.Column(db.Integer, ForeignKey("topic.id"), nullable=True)