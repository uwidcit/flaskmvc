from App.database import db
from sqlalchemy import ForeignKey

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.String(500), nullable=False)
    library_id = db.Column(db.Integer, ForeignKey("library.id"), nullable=True)

    def addToLibrary(library_id):
        self.library_id = library_id
