from App.database import db

class Programme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree_name = db.Column(db.String(255))
    courses = db.relationship('Course', secondary='programme_course', back_populates='programmes', lazy='dynamic')

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)
            db.session.commit()
        return self

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            db.session.commit()
        return self
