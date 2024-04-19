from App.database import db

class Routine(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    routineName=db.Column(db.String(120),nullable=False)
    work=db.Relationship('Workout', backref='rout')

    
    
    # def addWorkout(self,exercise,name,difficulty,bSets,iSets,eSets,equipment,video,muscle,des):
    #     routine=Workout.query.filterby(exercise=exercise,id=self.id).first() #check if user has this exercise added 
    #     if not routine:
    #         routine=Workout(muscle=muscle,exercise=exercise,difficulty=difficulty,beginner_sets=bSets,intermediate_sets=iSets,expert_sets=eSets,equipment=equipment,description=des,video=video)
    #         db.session.add(routine)
    #         db.session.commit()
    #         return routine
    #     else:
    #         return None
    
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
