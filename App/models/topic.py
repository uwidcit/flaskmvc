import enum
from flask_sqlalchemy import SQLAlchemy

from .subscription import Subscription

db = SQLAlchemy()

class Level(enum.Enum):
    ZERO = "ZERO"
    ONE = "ONE"

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    level = db.Column(db.Enum(Level), default=Level.ZERO)
    posts = db.relationship("Post", backref="topic", lazy=True)

    def __repr__(self):
        return f"{self.text}"
 
    def get_post_count(self):
        return len(self.posts)

    def get_posts_json(self):
        return [ post.toDict() for post in self.posts ]

    # TODO: Implement observer pattern
    def subscribe(self, userId):
        sub = Subscription.query.filter_by(userId=userId, topicId=self.id)
        if sub:
            sub.set_active()
        else:
            new_sub = Subscription(userId=userId, topicId=self.id)
            db.session.add(new_sub)
            db.session.commit()
        

    def unsubscribe(self, userId):
        sub = Subscription.query.filter_by(userId=userId, topicId=self.id)
        if sub :
            sub.set_inactive()

    def toDict(self):
        return {
            "text": self.text,
            "level": self.level
        }
