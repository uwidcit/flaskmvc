from App.database import db
class Prerequisites(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    prereq_courseCode = db.Column(db.ForeignKey('course.courseCode'))
    courseName = db.Column(db.String(25))

    associated_course = db.relationship('Course', back_populates='prerequisites', overlaps="courses")
    
    

    def __init__(self, prereqCode, nameofCourse):
        self.prereq_courseCode = prereqCode
        self.courseName = nameofCourse

    def get_json(self):
        return{
            'prereq_id': self.id,
            'prerequisite_courseCode': self.prereq_courseCode,
            'prerequisite_course':self.courseName
        } 