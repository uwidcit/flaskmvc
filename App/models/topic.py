from flask_sqlalchemy import SQLAlchemy

from models import Subscription

# init db
db = SQLAlchemy()


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    level = db.Column(db.Integer, nullable=False) 
    posts = db.relationship("Post", back_populates="topic")
            

    def __repr__(self):
        return f"{self.text}"

    @property
    def post_count(self):
        return len(self.posts)

    # TODO: Implement observer pattern
    def subscribe(userID,TopicId):
        createSubscribe = Subscription(userID=userID, TopicId=TopicId)
        print(f"Subscribed: {userID}")
        db.session.add(createSubscribe)
        db.session.commit()
        return createSubscribe

    def unsubscribe(userID, TopicId):
        deleteSubscribe = Subscription(userID=userID, TopicId=TopicId)
        print(f"Un-Subscribed: {userID}")
        db.session.delete(deleteSubscribe)
        db.session.commit()
        return deleteSubscribe

    def toDict(self):
        return {
            "text": self.text,
            "level": self.level
        }
