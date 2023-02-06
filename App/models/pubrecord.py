from App.database import db
from sqlalchemy import ForeignKey

class PubRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    researcher_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    publication_id = db.Column(db.Integer, ForeignKey("publication.id"), nullable=False)

    def __init__(self, researcher_id, publication_id):
        self.researcher_id = researcher_id
        self.publication_id = publication_id