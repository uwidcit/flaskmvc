from App.database import db
from sqlalchemy import ForeignKey

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    records = db.relationship("LibraryRecord", backref="library", lazy=True, cascade="all, delete-orphan")

    def __init__(self, user_id):
        self.user_id = user_id