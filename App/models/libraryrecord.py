from App.database import db
from sqlalchemy import ForeignKey

class LibraryRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, ForeignKey("library.id"), nullable=False)
    publication_id = db.Column(db.Integer, ForeignKey("publication.id"), nullable=False)

    def __init__(self, library_id, publication_id):
        self.library_id = library_id
        self.publication_id = publication_id