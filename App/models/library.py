from App.database import db
from sqlalchemy import ForeignKey

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    publications = db.relationship("Publication", backref="library")

    def __init__(self, user_id):
        self.user_id = user_id