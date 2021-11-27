from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Integer, db.ForeignKey('user.id'))
    created = db.relationship("Topic", back_populates="subscription")
    

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