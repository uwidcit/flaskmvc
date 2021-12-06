from datetime import datetime
from App.database import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(15), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        

    def __repr__(self):
        return f"{self.text}"

    def get_created_string(self):
        return self.created.strftime("%Y-%m-%dT%H:%M:%SZ")

    def toDict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created": self.get_created_string()
        }
