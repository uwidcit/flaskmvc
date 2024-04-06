from App.database import db
from App.constants import MIN_CODE_LENGTH, MAX_CODE_LENGTH, MIN_CODE_VALUE, MAX_CODE_VALUE
from sqlalchemy.orm import validates

# Should ONLY be instantiated if the guess has passed the Game model's validation, meaning it doesn't break any
#     of the constraints given for a valid code, nor those for a valid guess given the selected game's answer.
class UserGuess(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)

    # NOTE: Guess must be stored as a string instead of an int to preserve any leading zeroes
    guess = db.Column(db.String(MAX_CODE_LENGTH), db.CheckConstraint(
        f"guess >= {MIN_CODE_VALUE} AND guess <= {MAX_CODE_VALUE} AND LENGTH(guess) >= {MIN_CODE_LENGTH} AND LENGTH(guess) <= {MAX_CODE_LENGTH}"),
        nullable=False)
    
    @property
    def guess_length(self):
        return len(self.guess)
    
    user_relation = db.relationship("User", back_populates="guesses")
    game_relation = db.relationship("Game", back_populates="guesses")

    def __init__(self, user_id, game_id, guess):
        self.user_id = user_id
        self.user_attempts = game_id
        self.guess = guess
    
    def __repr__(self):
        return f'UserGuess({self.user_id}, {self.game_id}, {self.guess})'
    
    def __str__(self):
        return f"""
User Guess Info:
    |- User ID: {self.user_id}
    |- Game ID: {self.game_id}
    |- Guess: {self.guess}
"""
    
    def get_json(self):
        return {
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
        
        if not self.MIN_CODE_VALUE <= value_int <= self.MAX_CODE_VALUE:
            raise ValueError(f"expected guess to be within the range <{self.MIN_CODE_VALUE:0{self.MIN_CODE_LENGTH}d}> to <{self.MAX_CODE_VALUE}>, inclusive; recieved <{value}>")
        
        # Return the original string if all validation checks succeeded
        return value
