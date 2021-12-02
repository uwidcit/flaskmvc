from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

# init db
db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="posts")
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship("Topic", back_populates="posts")
    text = db.Column(db.String(200), nullable=False) 
    created = db.Column(db.Datetime, nullable=False, default=datetime.utcnow)
        

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
