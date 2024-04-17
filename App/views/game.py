from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from sqlalchemy.exc import IntegrityError

from App.controllers import get_curr_game
from App.database import db
from App.models import UserGuess
from datetime import datetime


game_views = Blueprint('game_views', __name__, template_folder='../templates')

@game_views.route('/game', methods=['GET'])
@jwt_required()
def game():
    today = datetime.utcnow().date()
    curr_game = get_curr_game()

    if not curr_game:
        return jsonify({"error" : "An error has occured whilst accessing today's game"}), 500

    guesses = UserGuess.get_guesses(curr_game.id, jwt_current_user.id)
    curr_game_json = curr_game.get_json()

    # Evaluate the last guess to get the guess results
    prev_guess = guesses[-1].guess if guesses else None
    verdict = curr_game.evaluateGuess(prev_guess) if prev_guess else None

    return render_template('game.html', 
                            curr_game=curr_game_json, 
                            today=today, 
                            guesses=guesses, 
                            verdict=verdict)

@game_views.route('/evaluate_guess', methods=['POST'])
@jwt_required()
def evaluateGuess():
    user = jwt_current_user
    curr_game = get_curr_game()

    user_id = user.id
    game_id = curr_game.id
    
    guess = ''.join(request.form.get(f'guess-digit-{i}') for i in range(curr_game.answer_length))

    try:
        user_guess = UserGuess(user_id=user_id, game_id=game_id, guess=guess)
        db.session.add(user_guess)
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Failed To Submit Guess."}), 400

    return redirect(request.referrer)
