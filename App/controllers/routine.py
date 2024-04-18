# from App.models import Routine, Workout
# from App.database import db


# def create_routine(name, description, user_id):
#     routine = Routine(name=name, description=description, user_id=user_id)
#     db.session.add(routine)
#     db.session.commit()
#     return routine

# def get_all_routines():
#     return Routine.query.all()

# def get_routine(id):
#     return Routine.query.get(id)

# def get_user_routines(user_id):
#     return Routine.query.filter_by(user_id=user_id).all()

# def update_routine(id, name=None, description=None):
#     routine = Routine.query.get(id)
#     if name is not None:
#         routine.name = name
#     if description is not None:
#         routine.description = description
#     db.session.commit()
#     return routine

# def add_workout_to_routine(routine_id, workout_id):
#     routine = Routine.query.get(routine_id)
#     workout = Workout.query.get(workout_id)
#     routine.workouts.append(workout)
#     db.session.commit()

# def delete_routine(id):
#     routine = Routine.query.get(id)
#     db.session.delete(routine)
#     db.session.commit()
