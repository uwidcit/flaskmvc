from App.database import db

class Routine(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    routineName=db.Column(db.String(120),nullable=False)
    work=db.Relationship('Workout', backref='rout')

    
    
    
    
    # def viewWorkout(self,exercise):
        
    #     return None

    # def removeWorkout(self,exercise):
    #     workout_name=Workout.query.filterby(exercise=exercise,id=self.id)
    #     if workout_name:
    #         db.session.delete(workout_name)
    #         db.session.commit()
    #         return True
    #     return None
    
    def get_json(self):
        return {
            self.routineName
        }

        return None
