class CoursePlanCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    difficulty = db.Column(db.Integer)
    semester_available = db.Column(db.Integer)
    year = db.Column(db.Integer)
    course_plan_id = db.Column(db.Integer, db.ForeignKey('course_plan.plan_id'), nullable=False)