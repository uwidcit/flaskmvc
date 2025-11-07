from App.database import db

class Shortlist(db.Model):

    shortlist_id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.internship_id'), nullable=False)  # FIXED
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=True)
    status = db.Column(db.String(50), nullable=True)  # accepted, rejected


    def __init__(self, internship_id, staff_id, student_id, status=None):
        self.internship_id = internship_id
        self.staff_id = staff_id
        self.student_id = student_id
        self.status = status

    def get_json(self):
        return {
            'shortlist_id': self.shortlist_id,
            'internship_id': self.internship_id,
            'staff_id': self.staff_id,
            'student_id': self.student_id,
            'status': self.status
            
        }

