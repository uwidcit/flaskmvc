from App.database import db

#Competitions Model
class Competition(db.Model):
    competition_ID = db.Column(db.Integer, primary_key=True)
    competition_Name = db.Column(db.String, nullable=False)
    date_occurred = db.Column(db.DateTime, nullable=False)
    competition_description = db.Column(db.String, nullable=True)

    def __init__(self, competition_Name, date_occurred, competition_description=None):
        self.competition_Name = competition_Name
        self.date_occurred = date_occurred
        self.competition_description = competition_description

    def get_json(self):
        return {
            'Competition ID': self.competition_ID,
            'Competition Name': self.competition_Name,
            'Date Occurred': self.date_occurred.strftime('%Y-%m-%d'),
            'Competition Description': self.competition_description
        }

#Results Model 
class CompetitionResult(db.Model):
    result_ID = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competition.competition_ID'), nullable=False)
    student = db.Column(db.String, nullable=False)
    result = db.Column(db.Float, nullable=False)

    competition = db.relationship('Competition', backref='results')

    def __init__(self, competition_id, student, result):
        self.competition_id = competition_id
        self.student = student
        self.result = result

    def get_json(self):
        return {
            'result_ID': self.result_ID,
            'competition_id': self.competition_id,
            'student': self.student,
            'result': self.result
        }
