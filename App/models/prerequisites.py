from App.database import db


class Prerequisites(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(8), db.ForeignKey('course.courseCode'), primary_key=True)
    prereq_code = db.Column(db.String(8)) #Maybe also a foreignkey

    
    course = db.relationship('Course', foreign_keys=[course_id], backref='prerequisite_rel')
    #course = db.relationship('Course', back_populates='prerequisites_rel')
    #prereq_course = db.relationship('Course', foreign_keys=[prereq_code], back_populates='prerequisites_for')

    def __init__(self, course_id, prereq_code):
        self.course_id = course_id
        self.prereq_code = prereq_code

    def get_json(self):
            return{
                'prereq_id': self.id,
                'course_id': self.course_id,
                'prerequisite_course': self.prereq_code,
            }