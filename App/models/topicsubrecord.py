from App.database import db
from sqlalchemy import ForeignKey

class TopicSubRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    topic_id = db.Column(db.Integer, ForeignKey("topic.id"), nullable=False)

    def __init__(self, user_id, topic_id):
        self.user_id = user_id
        self.topic_id = topic_id