from App.models import Game
from App.database import db
from datetime import datetime

def create_game(max_attempts, preset_answer=None, answer_length=None):
    try:
        newGame = Game(max_attempts, preset_answer, answer_length)
        db.session.add(newGame)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return None
    else:
        return newGame
    
def get_curr_game():
    current_date = datetime.utcnow().date()
    curr_game = Game.query.filter_by(creation_date=current_date).first()

    if not curr_game:
        # Temporary parameters for development purposes
        curr_game = create_game(5, answer_length=4)
    print(f"\nAnswer = {curr_game.answer}\n")
    return curr_game
