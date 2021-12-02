from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id')) 
    TopicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    

    def __init__(self, userID, topicId):
        self.userID = userID
        self.TopicId = TopicId
        

    def __repr__(self):
        return f"{self.userID}"


    def toDict(self):
        return {
            "userID": self.userID,
            "TopicId": self.TopicId
        }
