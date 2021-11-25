from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    topicid = db.relationship("Topic", back_populates="post")
    text = db.relationship("Topic",back_populates="post")
    created = db.Column(db.Boolean, default=False, nullable=False)
    

    def __init__(self, userID, topicid, text, created):
        self.userID = userID
        self.topicid = topicid
        self.text = text
        self.created = created
        

    def __repr__(self):
        return f"{self.userID}"

    
    #def notifySubscribers(self, subscribers):
        #self.created = subscribers


    def toDict(self):
        return {
            "userID": self.userID,
            "topicid": self.topicid,
            "text": self.text,
            "created": self.created
        }
