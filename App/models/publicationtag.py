from App.database import db
from sqlalchemy import ForeignKey

class PublicationTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, ForeignKey("publication.id"), nullable=False)
    topic_id = db.Column(db.Integer, ForeignKey("topic.id"), nullable=False)

    def __init__(self, publication_id, topic_id):
        self.publication_id = publication_id
        self.topic_id = topic_id