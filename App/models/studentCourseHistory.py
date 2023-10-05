from App.database import db

class StudentCourseHistory(db.Model):
    __tablename__ = 'studentCourses'
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.ForeignKey('student.id'))
    code = db.Column(db.ForeignKey('course.courseCode'))

    associated_course = db.relationship('Course', back_populates='students', overlaps="courses")
    associated_student = db.relationship('Student', back_populates='courses', overlaps="student")

    def __init__(self, id, courseCode):
        self.studentID = id
        self.code = courseCode
    
    def get_json(self):
        return{
            'Program ID:': self.program_id,
            'Course Code: ': self.code,
            'Course Type: ': self.courseType
        }