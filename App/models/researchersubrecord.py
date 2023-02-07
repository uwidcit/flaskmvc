from App.database import db
from sqlalchemy import ForeignKey

class ResearcherSubRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    researcher_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)

    def __init__(self, user_id, researcher_id):
        self.user_id = user_id
        self.researcher_id = researcher_id