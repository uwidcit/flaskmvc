from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(15), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
        

    def __repr__(self):
        return f"{self.text}"

    def get_created_string(self):
        return created.strftime("%m/%d/%Y, %H:%M:%S")

    def toDict(self):
        return {
            "id": self.id,
            "text": self.text,
            "created": self.get_created_string()
        }
