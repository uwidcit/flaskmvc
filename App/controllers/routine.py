from App.models import Routine
from App.database import db

def create_routine(userID, routineName):
    routine = Routine.query.get(routineName) #check if routine exists
    if routine:
        return None
    
    new_routine = Routine(userID=userID, routineName=routineName)
    db.session.add(new_routine)
    db.session.commit()
    return new_routine

def get_all_routines():
    return Routine.query.all()

def get_routine_by_id(id):
    return Routine.query.get(id)


def delete_routine(id):
    routine=Routine.query.filter_by(id=id)

    if routine:
        db.session.delete(routine)
        db.session.commit()
        return True
    else:
        return False

def renameRoutine(oldname,routineName):
    routine=Routine.query.filter_by(routineName=oldname)

    if routine:
        routine.routineName=routineName
        db.session.add(routine)
        db.session.commit()
        return True
    else:
        return False


