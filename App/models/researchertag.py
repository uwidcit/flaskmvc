from App.database import db
from sqlalchemy import ForeignKey

class ResearcherTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    researcher_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    topic_id = db.Column(db.Integer, ForeignKey("topic.id"), nullable=False)

    def __init__(self, researcher_id, topic_id):
        self.researcher_id = researcher_id
        self.topic_id = topic_id