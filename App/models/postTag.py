from . import db


class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagId = db.Column(db.Integer, db.ForeignKey('tag.id'))
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    

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