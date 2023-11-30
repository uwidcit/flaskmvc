from App.database import db


class CoursePlan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    year = db.Column(db.Integer, default=db.func.current_date().year)
    semester = db.Column(db.Integer)
    courses = relationship('CoursePlanCourse', backref='course_plan', lazy=True)