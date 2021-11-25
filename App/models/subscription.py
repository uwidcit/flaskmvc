from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    Topicid = db.relationship("Topic", back_populates="subscription")
    

    def __init__(self, userID, topicid):
        self.userID = userID
        self.Topicid = Topicid
        

    def __repr__(self):
        return f"{self.userID}"


    def toDict(self):
        return {
            "userID": self.userID,
            "Topicid": self.Topicid
        }
