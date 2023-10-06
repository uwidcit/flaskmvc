from App.database import db


class CoursePlanCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planId = db.Column(db.ForeignKey('course_plan.planId'))
    code = db.Column(db.ForeignKey('course.courseCode'))
    
    # associated_coursePlan = db.relationship('CoursePlan', back_populates='students', overlaps="coursePlan")
    # associated_course = db.relationship('Course', back_populates='planIds', overlaps="courses")

    def __init__(self, username, password, name, program_id):
        self.id = username
        self.name = name
        self.program_id = program_id

    def get_json(self):
        return{
            'student_id': self.id,
            'name': self.name,
            'program' : self.program_id
        }

