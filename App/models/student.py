from App.models import Programme, History, CoursePlan
from App.database import db

class Student(User):
    programme_id = db.Column(db.Integer, db.ForeignKey('programme.id'))
    programme = db.relationship('Programme', back_populates='students')
    academic_history = db.relationship('History', backref='student', lazy=True)
    academic_plan = db.relationship('CoursePlan', backref='student', lazy=True)

    def enroll_in_programme(self, programme):
        if self.programme:
            return f"Error: {self.name} is already enrolled in the {self.programme.degree_name} programme."
            
        self.programme = programme
        db.session.commit()
        return self.programme

    def create_course_plan(self, programme, academic_history):  #tbis need work
        course_plan = CoursePlan(student=self)
        db.session.add(course_plan)
        db.session.commit()
        return course_plan

    def view_course_plan(self):
        return self.academic_plan
