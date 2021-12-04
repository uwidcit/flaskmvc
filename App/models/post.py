from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="posts")
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship("Topic", back_populates="posts")
    text = db.Column(db.String(200), nullable=False) 
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        

    def __repr__(self):
        return f"{self.user_id}"

    
    def notifySubscribers(self, subscribers):
        self.text = subscribers


    def toDict(self):
        return {
            "user_id": self.user_id,
            "topicId": self.topicId,
            "text": self.text,
            "created": self.created
        }
