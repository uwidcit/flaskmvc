from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    text = db.Column(db.String(200), nullable=False) 
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.relationship('Tag', lazy=True, backref="posts")
  
        

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
