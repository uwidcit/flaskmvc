from App.database import db

class StudentModel (db.Model):
    _id = db.Column("id", db.Integer, primary_key=True,nullable=False)
    studentId = db.Column(db.Integer, unique=True , nullable=False)
    name = db.Column(db.String(120), nullable=False)
    karma = db.Column(db.Float)
    # reviews = db.relationship('Reviews', backref=db.backref('StudentModel', lazy='joined'))

    def __init__(self, studentId, name):
        self.studentId = studentId
        self.name = name
        self.karma = 0.0
        #self.reviews = reviews

    def toJSON(self):
        return{
            # 'reviewId': self.reviewId,
            'id': self._id,
            'studentId': self.studentId,
            'name': self.name,
            'karma': self.karma,  
        }