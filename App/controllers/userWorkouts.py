from App.models import Routine,UserWorkouts
from App.database import db



def addToRoutine(routine_id,workout_id):
    exists=UserWorkouts.query.filter_by(routine_id=routine_id,workout_id=workout_id).first() # check to see if workout exists within this routine

    if exists:
        return False
    else:
        workout=UserWorkouts(workout_id,routine_id)
        db.session.add(workout)
        db.session.commit()
        return True

def removeWorkout(routine_id,workout_id):
    workout=UserWorkouts.query.filter_by(routine_id=routine_id,workout_id=workout_id).first() 

    if workout:
        db.session.delete(workout)
        db.session.commit()
        return True
    else:
        return False
