from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Subtopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subtext = db.Column(db.String(300), nullable=False)
    postID = db.Column(db.Integer, db.ForeignKey('post.id'))
    

    def __init__(self, subtext, postID):
        self.subtext = subtext
        self.postID = postID
        

    def __repr__(self):
        return f"{self.subtext}"


    def toDict(self):
        return {
            "subtext": self.subtext,
            "postID": self.postID
        }
