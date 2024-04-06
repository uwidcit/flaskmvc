from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/game', methods=['GET'])
def game():
    answer_length = 5
    return render_template('game.html', answer_length=5)

def evaluateGuess():
    pass