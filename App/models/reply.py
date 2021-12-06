from sqlalchemy.orm import backref
from App.database import db
from App.models import Post

class Reply(Post):
    __mapper_args__ = {'polymorphic_identity': 'reply'}

    originalPostId = db.Column(db.Integer, db.ForeignKey('post.id'))
    originalPost = db.relationship('Post', backref='replies', remote_side='Post.id', lazy=True)

    def __init__(self, originalPostId):
        self.originalPostId = originalPostId

    def __repr__(self):
        return f"{self.originalPostId}"

    def toDict(self):
        return {
            "originalPostId": self.originalPostId
        }