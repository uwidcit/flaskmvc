from App.models import Workout
from App.database import db
# import os,json,jsonify
from dotenv import load_dotenv
import http.client


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


def addWorkout(self,exercise,name,difficulty,bSets,iSets,eSets,equipment,video,muscle,des):
        routine=Workout.query.filterby(exercise=exercise,id=self.id).first() #check if user has this exercise added 
        if not routine:
            routine=Workout(muscle=muscle,exercise=exercise,difficulty=difficulty,beginner_sets=bSets,intermediate_sets=iSets,expert_sets=eSets,equipment=equipment,description=des,video=video)
            db.session.add(routine)
            db.session.commit()
            return routine
        else:
            return None

def removeWorkout(self,exercise):
        workout_name=Workout.query.filterby(exercise=exercise,id=self.id)
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

#return a type of exercise
def fetch_workout(param):
    load_dotenv()
    api_key=os.getenv("API_KEY")

    conn = http.client.HTTPSConnection("work-out-api1.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "work-out-api1.p.rapidapi.com"
}
    conn.request("GET", f"/search?WorkOut={param}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode('utf-8')


#Choose type of data and category
#types in workout model under api tags
def fetch_data(type,param):
    load_dotenv()
    api_key=os.getenv("API_KEY")

    conn = http.client.HTTPSConnection("work-out-api1.p.rapidapi.com")

    headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "work-out-api1.p.rapidapi.com"
}
    conn.request("GET", f"/search?{type}={param}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode('utf-8')