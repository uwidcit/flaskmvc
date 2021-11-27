from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagId = db.Column(db.Integer, db.ForeignKey('user.id'))
    postId = db.relationship("Topic", back_populates="subscription")
    

    def __init__(self, tagId, postId):
        self.tagId = tagId
        self.postId = postId
        

    def __repr__(self):
        return f"{self.tagId}"


    def toDict(self):
        return {
            "tagId": self.tagId,
            "postId": self.postId
        }