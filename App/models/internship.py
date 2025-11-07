from App.database import db

class Internship(db.Model):
    internship_id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    shortlist = db.relationship('Shortlist', backref=db.backref('internship', lazy='joined'))
    
    def __init__(self, title, description, employer_id):
        self.title = title
        self.description = description
        self.employer_id = employer_id

    def get_json(self):
        return {
            'internship_id': self.internship_id,
            'title': self.title,
            'description': self.description,
            'employer_id': self.employer_id
        }


