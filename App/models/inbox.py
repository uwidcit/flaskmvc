from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Inbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    postId = db.Column(db.Integer, db.ForeignKey('post.id'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    read = db.Column(db.Boolean,default=False, nullable=False)
    notified = db.Column(db.Boolean, default=False, nullable=False)
    

    def __init__(self, postId, userId, read, notified):
        self.postId = postId
        self.userId = userId
        self.read = read
        self.notified = notified
        

    def __repr__(self):
        return f"{self.postId}"

    #def sendNotification(self, notification):
        #self.notified = notification

    def toDict(self):
        return {
            "postId": self.postId,
            "userId": self.userId,
            "read": self.read,
            "notified": self.notified
        }
