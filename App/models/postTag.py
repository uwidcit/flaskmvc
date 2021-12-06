from App.database import db

class PostTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagId = db.Column(db.Integer, db.ForeignKey('tag.id'))
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    tag = db.relationship("Tag", lazy=True, backref="tag")
    

    def __init__(self, tagId, postId):
        self.tagId = tagId
        self.postId = postId
        
    def __repr__(self):
        return f"PostTag({self.tagId}, {self.postId})"

    def get_posts_json(self):
        return [ post.to_dict() for post in self.posts ] 

    def toDict(self):
        return {
            "id": self.id,
            "tagId": self.tagId,
            "postId": self.postId
        }