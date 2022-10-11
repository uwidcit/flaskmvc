from App.database import db

class Reviews (db.Model):
    _id = db.Column("id", db.Integer, primary_key=True,nullable=False)
    studentId = db.Column(db.Integer, db.ForeignKey('studentModel.studentId'))
    message = db.Column(db.String(300), nullable=False)
    upvote = db.Column(db.Integer, nullable = True)
    downvote = db.Column(db.Integer, nullable = True)
 
    def __init__(self,studentId, message, upvote, downvote):
        self.studentId = studentId
        self.message = message
        self.upvote = upvote
        self.downvote = downvote
    
    def toJSON(self):
        return{
            'id': self._id,
            'studentId': self.studentId,
            'message': self.message,
            'upvote': self.upvote,
            'downvote': self.downvote,  
        }