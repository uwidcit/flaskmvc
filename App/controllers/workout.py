from App.models import Workout
from App.database import db

def get_workout(workoutID):
    return Workout.query.get(workoutID)

def get_workout_by_name(workout_name):
    return Workout.query.filter_by(name=workout_name).first()

def get_all_workouts():
    return Workout.query.all()

def get_all_workouts_json():
    workouts = Workout.query.all()
    if not workouts:
        return []
    workouts = [workout.get_json() for workout in workouts]
    return workouts