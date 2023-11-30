from App.database import db

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    semester_courses = db.relationship('CourseHistory', backref='history', lazy=True)
    