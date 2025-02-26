from App.database import db

class Assignee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=True)

    room = db.relationship('Room', backref=db.backref('assignees', lazy=True))

    def __init__(self, fname, lname, email, room_id=None):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.room_id = room_id

    def get_json(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'room_id': self.room_id
        }

    def __repr__(self):
        return f'<Assignee {self.fname} {self.lname}, Room ID: {self.room_id}>'
    
    def __str__(self):
        return f'{self.fname} {self.lname}'

