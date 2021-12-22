from App.database import db
from App.models import Post


class Reply(Post):
    __mapper_args__ = {'polymorphic_identity': 'reply'}

    originalPostId = db.Column(db.Integer, db.ForeignKey('post.id'))
    originalPost = db.relationship('Post', backref='replies', remote_side='Post.id', lazy=True)

    def __init__(self, originalPostId, user_id, topic_id, text, created):
        super().__init__(user_id, topic_id, text, created)        
        self.originalPostId = originalPostId


    def __repr__(self):
        return f"Reply({self.originalPostId})"


    def toDict(self):
        propertyDict = super().toDict()
        propertyDict["originalPostId"] = self.originalPostId

        return propertyDict

        # return {
        #     "id": self.id,
        #     "originalPostId": self.originalPostId
        # }
