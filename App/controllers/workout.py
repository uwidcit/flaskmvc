from App.models import Workout
from App.database import db
import os,json,jsonify
from dotenv import load_dotenv
import http.client


def get_workout(workoutID):
    return Workout.query.get(workoutID)

def get_workout_by_name(workout_name):
    return Workout.query.filter_by(exercise=workout_name).first()

def get_all_workouts():
    return Workout.query.all()

def get_all_workouts_json():
    workouts = Workout.query.all()
    if not workouts:
        return []
    workouts = [workout.get_json() for workout in workouts]
    return workouts

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