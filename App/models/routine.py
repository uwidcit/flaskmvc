from App.database import db

class Routine(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    routineName=db.Column(db.String(120),nullable=False)
    
    
    def addWorkout(self,workouts,routineID,id):
        routine=Routine.query.get(routineID)
        if routine.userID==id:
            return None
    
    def viewWorkout(self,workoutId):
        return None

    def removeWorkout(self,workoutId):
        return None

    def get_json(self):
        return None
