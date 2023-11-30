from App.database import db

class HistoryCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('history.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    passed = db.Column(db.Boolean, default=False)

    def course_passed(self):
        return self.passed