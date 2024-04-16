from App.models import Routine
from App.database import db

def create_routine(routineID, routineName):
    routine = Routine.query.get(routineID)
    if routine:
        return None
    
    new_routine = Routine(id=routineID, routineName=routineName)
    db.session.add(new_routine)
    db.session.commit()
    return new_routine

def get_all_routines():
    return Routine.query.all()

def get_routine_by_name(routineName):
    return Routine.query.get(routineName)