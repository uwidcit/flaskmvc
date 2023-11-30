from App.database import db
from enum import Enum

class CourseType(Enum):
    CORE = 'core'
    ELECTIVE = 'elective'

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(255))
    course_code = db.Column(db.String(20), unique=True)
    credits = db.Column(db.Integer)
    course_type = db.Column(db.Enum(CourseType))
    dept = db.Column(db.String(50))
    
    prerequisites = db.relationship('Course', secondary='course_prerequisite', primaryjoin='Course.id==course_prerequisite.c.course_id', secondaryjoin='Course.id==course_prerequisite.c.prerequisite_id', back_populates='successor_courses', lazy='dynamic')
    anti_requisites = db.relationship('Course', secondary='course_antirequisite', primaryjoin='Course.id==course_antirequisite.c.course_id', secondaryjoin='Course.id==course_antirequisite.c.antirequisite_id', lazy='dynamic')
    successor_courses = db.relationship('Course', secondary='course_prerequisite', primaryjoin='Course.id==course_prerequisite.c.prerequisite_id', secondaryjoin='Course.id==course_prerequisite.c.course_id', back_populates='prerequisites', lazy='dynamic')
    
    def add_course_to_list(self, other_course, course_list):
        if course_list == 'prerequisites':
            if other_course not in self.prerequisites:
                self.prerequisites.append(other_course)
        elif course_list == 'anti_requisites':
            if other_course not in self.anti_requisites:
                self.anti_requisites.append(other_course)
        elif course_list == 'successor_courses':
            if other_course not in self.successor_courses:
                self.successor_courses.append(other_course)
        db.session.commit()
        return getattr(self, course_list)

    def remove_course_from_list(self, other_course, course_list):
        if course_list == 'prerequisites':
            if other_course in self.prerequisites:
                self.prerequisites.remove(other_course)
        elif course_list == 'anti_requisites':
            if other_course in self.anti_requisites:
                self.anti_requisites.remove(other_course)
        elif course_list == 'successor_courses':
            if other_course in self.successor_courses:
                self.successor_courses.remove(other_course)
        db.session.commit()
        return getattr(self, course_list)


course_prerequisite = db.Table('course_prerequisite',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('prerequisite_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

course_antirequisite = db.Table('course_antirequisite',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('antirequisite_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)
