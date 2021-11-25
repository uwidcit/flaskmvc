from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    level = db.relationship("Admin",back_populates="topic")
    

    def __init__(self, text, level):
        self.text = text
        self.level = level
        

    def __repr__(self):
        return f"{self.text}"

    #def subscribe(self, userId):
        #self.level = userId

    #def unsubscribe(self, userId):
        #self.level = userId

    def toDict(self):
        return {
            "text": self.text,
            "level": self.level
        }
