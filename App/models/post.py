from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="posts")
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    topic = db.relationship("Topic", back_populates="posts")
    text = db.Column(db.String(200), nullable=False)
    created = db.Column(db.Boolean, default=False, nullable=False)
        

    def __repr__(self):
        return f"{self.user_id}"

    
    def notifySubscribers(self, subscribers):
        self.text = subscribers


    def toDict(self):
        return {
            "user_id": self.user_id,
            "topic_id": self.topic_id,
            "text": self.text,
            "created": self.created
        }
