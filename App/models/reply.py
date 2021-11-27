from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    originalPostId = db.Column(db.Integer, db.ForeignKey('post.id'))
    

    def __init__(self, originalPostId):
        self.originalPostId = originalPostId
        

    def __repr__(self):
        return f"{self.originalPostId}"


    def toDict(self):
        return {
            "originalPostId": self.originalPostId
        }