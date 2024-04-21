from App.database import db


class UserWorkouts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    workout_id=db.Column(db.Integer,db.ForeignKey('workout.id'))
    routine_id=db.Column(db.Integer, db.ForeignKey('routine.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


    def __init__(self,workout_id,routine_id):
        self.workout_id=workout_id
        self.routine_id=routine_id