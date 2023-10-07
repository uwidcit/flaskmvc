from App.database import db

class CoursePlan(db.Model):
    planId=db.Column(db.Integer, primary_key=True)
    studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)
    
    student = db.relationship('Student', backref=db.backref('course_plans', uselist=True))

    # courses = db.relationship('CoursePlanCourses', backref = 'coursePlan', lazy=True)

    def __init__(self, studentid, ):
        self.studentId = studentid
        

    def get_json(self):
        return{
            'planId': self.planId,
            'studentId': self.studentId,
        }