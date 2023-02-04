from App.database import db

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    publications = db.relationship("Publication", backref="library")