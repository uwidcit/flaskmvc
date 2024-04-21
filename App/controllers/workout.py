from App.models import Workout
from App.database import db
# import os,json,jsonify
from dotenv import load_dotenv
import http.client
import os, json

def get_workout(workoutID):
    return Workout.query.get(workoutID)

def get_workout_by_name(workout_name):
    work=Workout.query.filter_by(exercise=workout_name).first()
    if work:
        return work
    else:
        work=fetch_workout(workout_name)
        return work

def get_all_workouts():
    return Workout.query.all()

def get_all_workouts_json():
    workouts = Workout.query.all()
    if not workouts:
        return []
    workouts = [workout.get_json() for workout in workouts]
    return workouts

def get_workout_by_type(muscle_type):
    workouts=Workout.query.filter_by(muscle=muscle_type).all()
    return workouts

def removeWorkout(self,exercise):
        workout_name=Workout.query.filter_by(exercise=exercise,id=self.id)
        if workout_name:
            db.session.delete(workout_name)
            db.session.commit()
            return True
        return None

#Input type of muscle and returns exercises related to that 
def fetch_muscle(param):
    load_dotenv()
    api_key=os.getenv("API_KEY")

    conn = http.client.HTTPSConnection("work-out-api1.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "work-out-api1.p.rapidapi.com"
}
    conn.request("GET", f"/search?Muscles={param}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode('utf-8')





##POPULATE DATABASE ####
def addWorkout(exercise,difficulty,bSets,iSets,eSets,equipment,video,muscle,des):
        routine=Workout.query.filter_by(exercise=exercise).first()#check if this exercise exist 
        if not routine:
            routine=Workout(muscle=muscle,exercise=exercise,difficulty=difficulty,beginner_sets=bSets,intermediate_sets=iSets,expert_sets=eSets,equipment=equipment,description=des,video=video)
            db.session.add(routine)
            db.session.commit()
            return routine
        else:
            return None



def load_db():
    muscle_types=['Biceps','Chest','Glutes','Abs','Lats','Back',
    'Legs','Stretching','Warm_Up','Hamstring','Calves','Quadriceps',
    'Trapezius','Shoulders','Triceps']

    #  workouts= set() # <-prevent duplicates

    for muscle in muscle_types:
        mus=fetch_muscle(muscle)
        mus=json.loads(mus)
        for data in mus:
            # exercise=data['WorkOut']
            new_workout=addWorkout(data['WorkOut'],data['Intensity_Level'],data['Beginner Sets'],data['Intermediate Sets'],data['Expert Sets'],data['Equipment'],data['Video'],data['Muscles'],data['Explaination'])

    print('Database populated')
    return None    