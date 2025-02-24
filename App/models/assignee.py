from App.database import db

class Assignee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique = True)  

    def __init__(self, fname, lname, email):
        self.fname = fname
        self.lname = lname
        self.email = email

    def get_json(self):
        return {
            'id': self.id,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email
        }

    def __repr__(self):
        return f'<Assignee {self.fname} {self.lname}>'
    
    def __str__(self):
        return f'{self.fname} {self.lname}'
