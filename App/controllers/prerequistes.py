from App.models import Prerequisites
from App.database import db

def create_prereq(prereqCode, courseName):
    prereq = Prerequisites(prereqCode, courseName)
    db.session.add(prereq)
    db.session.commit()

def get_all_prerequisites(courseName):
    return Prerequisites.query.filter(Prerequisites.courseName == courseName).all()

def getPrereqCodes(courseName):
    prereqs = get_all_prerequisites(courseName)
    codes = []

    for p in prereqs:
        codes.append(p.prereq_courseCode)
    
    return codes