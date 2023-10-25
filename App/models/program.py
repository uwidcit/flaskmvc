from App.database import db
class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    core_credits = db.Column(db.Integer)
    elective_credits = db.Column(db.Integer)
    foun_credits = db.Column(db.Integer)
    
    students = db.relationship('Student', backref='program', lazy=True)
    courses = db.relationship('ProgramCourses', backref='program', lazy=True)

    def __init__(self, name, core, elective, foun):
       self.name = name
       self.core_credits = core
       self.elective_credits = elective
       self.foun_credits = foun


    def get_json(self):
        return{
            'Program ID:': self.id,
            'Program Name: ': self.name,
            'Core Credits: ': self.core_credits,
            'Elective Credits ': self.elective_credits,
            'Foundation Credits: ': self.foun_credits,
        }
       