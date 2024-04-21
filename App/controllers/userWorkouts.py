from App.models import Routine,UserWorkouts,Workout
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

def viewWorkouts(routine_id):
    user_workout=UserWorkouts.query.filter_by(routine_id=routine_id).all()
    
    workout_ids = [user_workout.workout_id for user_workout in user_workouts] 
    workouts = Workout.query.filter(Workout.id.in_(workout_ids)).all()
    return workouts

