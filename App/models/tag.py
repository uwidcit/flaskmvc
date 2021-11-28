from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    created = db.Column(db.Boolean, default=False, nullable=False)
    

    def __init__(self, text, created):
        self.text = text
        self.created = created
        

    def __repr__(self):
        return f"{self.text}"


    def toDict(self):
        return {
            "text": self.text,
            "created": self.created
        }