from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from App.controllers import get_curr_game
from datetime import date


game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/game', methods=['GET'])
def game():
    curr_game = get_curr_game()

    if not curr_game:
        return jsonify({"error" : "An error has occured whilst accessing today's game"}), 500
    
    curr_game_json = curr_game.get_json()

    return render_template('game.html', curr_game=curr_game_json)

def evaluateGuess():
    pass