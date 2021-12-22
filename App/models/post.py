from App.database import db
from datetime import datetime

from App.modules.serialization_module import serialize_list

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    text = db.Column(db.String(200), nullable=False) 
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.relationship('PostTag', lazy=True, backref="post")
        

    def __init__(self, user_id, topic_id, text, created):
        self.userId = user_id
        self.topicId = topic_id
        self.text = text
        self.created = created


    def __repr__(self):
        return f"{self.userId}"

    
    def notifySubscribers(self, subscribers):
        self.text = subscribers

    def get_created_string(self):
        return self.created.strftime("%Y-%m-%dT%H:%M:%SZ")


    def toDict(self):
        return {
            "id": self.id,
            "user_id": self.userId,
            "topicId": self.topicId,
            "text": self.text,
            "created": self.get_created_string(),
            "tags": serialize_list(list(map(lambda postTag: postTag.tag, self.tags)))
        }
