from App.database import db
class ProgramCourses(db.Model):
    __tablename__ ='program_courses'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.ForeignKey('program.id'))
    code = db.Column(db.ForeignKey('course.courseCode'))
    courseType = db.Column(db.Integer)

    associated_program = db.relationship('Program', back_populates='courses', overlaps="program")
    associated_course = db.relationship('Course', back_populates='programs', overlaps="courses")

    def __init__(self, programID, courseCode, num):
        self.program_id = programID
        self.code = courseCode
        self.courseType = num
    
    def get_json(self):
        return{
            'Program Course ID:' : self.id,
            'Program ID:': self.program_id,
            'Course Code: ': self.code,
            'Course Type: ': self.courseType
        }