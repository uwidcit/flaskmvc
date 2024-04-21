from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,url_for
from App.models import db
from App.controllers.auth import jwt_required
from App.controllers.workout import *
import json

# from App.controllers import (
#     addWorkout,
#     remove_workout
# )

all_workouts_views= Blueprint('all_workouts_views', __name__, template_folder='../templates')


@all_workouts_views.route('/', methods=['GET'])
def workout_page():
    
    load_db()
        
    all_workouts={
        "Muscles":{
            "Biceps":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Biceps.jpg?v=1601051495",
            "Chest":"https://th.bing.com/th/id/R.0c90b0441cc12ddf6ae38104eb8e3499?rik=C60VmMRY78KgpQ&pid=ImgRaw&r=0",
            "Triceps":"https://th.bing.com/th/id/OIP.nevwTCxvTYZFIO063lQEtgHaEx?rs=1&pid=ImgDetMain",
            "Abs":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Abs.jpg?v=1601051622",
            "Back":"https://barbend.com/wp-content/uploads/2019/04/Back-Muscles.jpg",
            "Legs":"https://th.bing.com/th/id/OIP.ZtNjrRO69YDEYKa-53MqgQAAAA?rs=1&pid=ImgDetMain",
            "Stretching":"https://yourillust.com/wp-content/uploads/illustration-posts/woman-doing-chair-yoga-poses/woman-doing-chair-yoga-poses-thumbnail-1.jpg",
            "Warm_Up":"https://th.bing.com/th/id/R.7be822949cecca4c03dc29f0a1bfe5f2?rik=v4WFGEwHa7qCMA&pid=ImgRaw&r=0",
            "Lats":"https://www.oldschoollabs.com/wp-content/uploads/2020/08/Lats-Not-Just-for-Pull-ups.jpg",
            "Harmstring":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_hamstrings.jpg?v=1601051184",
            "Calves":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Calves.jpg?v=1601051316",
            "Quadriceps":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Quadriceps.jpg?v=1601051118",
            "Trapezius":"https://th.bing.com/th/id/OIP.M0-i-0v7yZ_4sNYB7SUoCAHaEK?rs=1&pid=ImgDetMain",
            "Shoulders":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Shoulders.jpg?v=1601051035",
            "Glutes":"https://cdn.shopify.com/s/files/1/1214/5580/files/Muscle_Group_Glutes.jpg?v=1601050628"
        },
        "Difficulty":{
            "Beginner":"https://th.bing.com/th/id/R.bf5c850f679326ee6e581ca83ffd4232?rik=9XLhCeQ%2b7As%2fkw&riu=http%3a%2f%2fwww.trainer.ae%2farticles%2fwp-content%2fuploads%2f2015%2f10%2fSkinny-guy-fat-world-1024x818.jpg&ehk=S69G6l3VB9MqBokSYC3X9Mc7Vn3pY9ptdpEUMWUvv00%3d&risl=&pid=ImgRaw&r=0",
            "Intermediate":"https://th.bing.com/th/id/R.70baadebbe59196467c8bfc24a1f5faa?rik=dtL%2fbAwczSfIFg&pid=ImgRaw&r=0",
            "Expert":"https://th.bing.com/th/id/R.9d8a75523660d8b06dc8584a20319008?rik=pUPFcOcvsQ8o2A&pid=ImgRaw&r=0"
        }
    }

    return render_template('all_workouts.html',all_workouts=all_workouts)


@all_workouts_views.route('/save_workout', methods=['POST'])
@jwt_required()
def save_workout():
    data=request.form
    current_user.addWorkout(data['Muscles'],data['WorkOut'],data['Difficulty'],data['Beginner Sets'],data['Intermediate Sets'],
    data['Expert Sets'],data['Equipment'],data['Explaination'],data['Video'])

    flash(f'{data["Muscles"]} workout saved')
    return render_template(request.referrer)

@all_workouts_views.route('/remove_workout', methods=['DELETE'])
@jwt_required()
def delete_workout():
    data=request.form
    current_user.delete_workout(data['WorkOut'])

    flash(f'{data["WorkOut"]} deleted')
    return render_template(request.referrer)





