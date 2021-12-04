from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from App.models import Post

class Reply(db.Model, Post):

    originalPostId = db.Column(db.Integer, db.ForeignKey('post.id'))
    originalPost = db.relationship('Post', backref='replies', lazy=True)

    def __init__(self, originalPostId):
        self.originalPostId = originalPostId

    def __repr__(self):
        return f"{self.originalPostId}"

    def toDict(self):
        return {
            "originalPostId": self.originalPostId
        }