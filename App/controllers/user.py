from App.models import User, Workout, Routine
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def create_routine(name, description, user_id):
    routine = Routine(name=name, description=description, user_id=user_id)
    db.session.add(routine)
    db.session.commit()
    return routine

def get_all_routines():
    return Routine.query.all()

def get_routine(id):
    return Routine.query.get(id)

def get_user_routines(user_id):
    return Routine.query.filter_by(user_id=user_id).all()

def update_routine(id, name=None, description=None):
    routine = Routine.query.get(id)
    if name is not None:
        routine.name = name
    if description is not None:
        routine.description = description
    db.session.commit()
    return routine

def add_workout_to_routine(routine_id, workout_id):
    routine = Routine.query.get(routine_id)
    workout = Workout.query.get(workout_id)
    routine.workouts.append(workout)
    db.session.commit()

def delete_routine(id):
    routine = Routine.query.get(id)
    db.session.delete(routine)
    db.session.commit()

