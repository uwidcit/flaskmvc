from App.database import db
from App.constants import MIN_CODE_LENGTH, MAX_CODE_LENGTH, MIN_CODE_VALUE, MAX_CODE_VALUE
from sqlalchemy.orm import validates

# Should ONLY be instantiated if the guess has passed the Game model's validation, meaning it doesn't break any
#     of the constraints given for a valid code, nor those for a valid guess given the selected game's answer.

class UserGuess(db.Model):
    # Removed the primary key contraints from user_id & game_id 
    # As it was preventing the player from making multiple guesses - Jay ~
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    # NOTE: Guess must be stored as a string instead of an int to preserve any leading zeroes
    guess = db.Column(db.String(MAX_CODE_LENGTH), db.CheckConstraint(
        f"CAST(guess AS INTEGER) >= {int(MIN_CODE_VALUE)} AND CAST(guess AS INTEGER) <= {int(MAX_CODE_VALUE)} AND LENGTH(guess) >= {MIN_CODE_LENGTH} AND LENGTH(guess) <= {MAX_CODE_LENGTH}"),
        nullable=False)
    
    @property
    def guess_length(self):
        return len(str(self.guess))
    
    user_relation = db.relationship("User", back_populates="guesses")
    game_relation = db.relationship("Game", back_populates="guesses")

    def __init__(self, user_id, game_id, guess):
        self.user_id = user_id
        self.game_id = game_id
        self.guess = guess
    
    def __repr__(self):
        return f'UserGuess({self.user_id}, {self.game_id}, {self.guess})'
    
    def __str__(self):
        return f"""
User Guess Info:
    |- ID: {self.id}
    |- User ID: {self.user_id}
    |- Game ID: {self.game_id}
    |- Guess: {self.guess}
"""
    
    def get_json(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'game_id': self.game_id,
            'guess': self.guess
        }
    
    # Validation function source: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators
    @validates("guess")
    def validate_guess(self, key, value):
        try:
            # Attempt to convert the guess string to an integer to check range validity
            value_int = int(value)
        except ValueError:
            # guess contained invalid characters or was the wrong type
            raise ValueError(f"could not cast guess of type <{value.__class__.__name__}> to type int")
        
        if not MIN_CODE_VALUE <= value_int <= MAX_CODE_VALUE:
            # Removed the self. temporarily as it was raising errors stating UserGuess has no attribute ''
            raise ValueError(f"expected guess to be within the range <{MIN_CODE_VALUE:0{MIN_CODE_LENGTH}d}> to <{MAX_CODE_VALUE}>, inclusive; recieved <{value}>")
        
        # Return the original string if all validation checks succeeded
        return value

    @classmethod
    def get_guesses(cls, game_id, user_id):
        # May want to store overall guess across multiple games
        # cls means Class| https://builtin.com/software-engineering-perspectives/python-cls
        return cls.query.filter_by(game_id=game_id, user_id=user_id).all()