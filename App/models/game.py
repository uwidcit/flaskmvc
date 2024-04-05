from App.database import db
from sqlalchemy.orm import validates
from random import randint
from datetime import datetime

class Game(db.Model):
    # valid answers/guesses range from 0123 (4 digits, maintain the leading zero) to 9_876_543_210 (10 digits); all digits unique
    __MIN_CODE_LENGTH = 4
    __MAX_CODE_LENGTH = 10
    __MIN_CODE_VALUE = 123
    __MAX_CODE_VALUE = 9_876_543_210


    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.DateTime, nullable=False, unique=True, default=datetime.datetime.today().date())
    max_attempts = db.Column(db.Integer, db.Constraint("max_attempts < 5"), nullable=False)

    # NOTE: Answer must be stored as a string instead of an int to preserve any leading zeroes
    answer = db.Column(db.String(__MAX_CODE_LENGTH), db.CheckConstraint(
        "LENGTH(answer) >= {__MIN_CODE_LENGTH} AND LENGTH(answer) <= {__MAX_CODE_LENGTH}"),
        nullable=False)
    answer_length = db.Column(db.Integer, db.CheckConstraint(
        f"answer_length >= {__MIN_CODE_LENGTH} AND answer_length <= {__MAX_CODE_LENGTH}"),
        nullable=False)
    
    guesses = db.relationship('UserGuess', back_populates='game_relation', cascade="all, delete-orphan")

    def __init__(self, max_attempts, preset_answer=None, answer_length=None):
        self.max_attempts = max_attempts

        # To preset an answer instead of randomly generating one, provide a value to the answer field.
        # Note that if an answer is preset, the answer length field will be discarded will discard the parameter
        #   value in favour of calculating it from the preset answer.
        if preset_answer is not None:
            self.answer = preset_answer
            self.answer_length = len(preset_answer)
        
        # If a specific answer is not provided, the answer is randomly generated
        #   using the provided answer length which MUST be provided.
        else:
            if answer_length is None:
                raise ValueError("MUST provide an answer length for random generation if not providing a specific answer")
            self.answer = self.generateAnswer(answer_length)

    def __repr__(self):
        return f'Game({self.max_attempts} : {self.answer})'
    
    def __str__(self):
        return f"""
Game Info:
    |- ID: {self.id}
    |- Creation Date: {self.creation_date}
    |- Max Attempts: {self.max_attempts}
    |- Answer: {self.answer}
    |- Answer length: {self.answer_length}
"""
    
    def get_json(self):
        return {
            'id' : self.id,
            'creation_date': {self.creation_date},
            'max_attempts': self.max_attempts,
            'answer': self.answer,
            'answer_length': self.answer_length
        }
    
    # Validation function source: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators

    @validates("max_attempts")
    def validate_max_attempts(self, key, value):
        pass

    @validates("answer")
    def validate_answer(self, key, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"answer value <{value}> could not be cast to type int")
        else:
            if not self.__MIN_CODE_VALUE <= value <= self.__MAX_CODE_VALUE:
                raise ValueError(f"provided answer must be within the range {self.__MIN_CODE_VALUE:0{self.__MIN_CODE_LENGTH}d} to {self.__MAX_CODE_VALUE}, inclusive)")
        return value
    
    @validates("answer_length")
    def validate_answer_length(self, key, value):
        if not self.__MIN_CODE_VALUE <= value <= self.__MAX_CODE_VALUE:
            raise ValueError(f"answer <{value}> is invalid")
        return value
    
    def generate_answer(self, answer_length):
        try:
            answer_length = int(answer_length)
        except ValueError:
            raise ValueError(f"provided answer length value <{answer_length}> contained not be cast to type int")
        
        if not (self.__MIN_CODE_LENGTH <= answer_length <= self.__MAX_CODE_LENGTH):
            raise ValueError(f"provided answer length must be within {self.__MIN_CODE_LENGTH} and {self.__MAX_CODE_LENGTH}, inclusive)")
        
        used_digits = []
        result = 0
        
        while len(result) < answer_length:
            temp = randint(0, 9)
            if temp not in used_digits:
                used_digits.append(temp)
                result = (result * 10) + temp
        return result        
    
    # Returns True if the guess adheres to the following:
    #   - Guess can be sucessfully cast to a positive integer within the valid range
    #   - Number of digit matches to answer (i.e., string length)
    #   - All digits in the guess are unique
    # Otherwise, returns False
    def __validateGuess(self, guess):
        try:
            # Attempt to cast to int to ensure no non-numerical characters
            guess = int(guess)

        except ValueError:
            raise ValueError(f"guess <{guess}> could not be cast to type int")
        
        else:
            if not (self.__MIN_CODE_LENGTH <= len(str(guess)) <= self.__MAX_CODE_LENGTH):
                raise ValueError(f"length of guess must be within {self.__MIN_CODE_LENGTH} and {self.__MAX_CODE_LENGTH} digits, inclusive)")
        
            if not (self.__MIN_CODE_VALUE <= guess <= self.__MAX_CODE_VALUE):
                raise ValueError(f"guess must be within the range {self.__MIN_CODE_VALUE:0{self.__MIN_CODE_LENGTH}d} and {self.__MAX_CODE_VALUE}, inclusive)")
        
        used_digits = []
        
        while len(result) < answer_length:
            temp = randint(0, 9)
            if temp not in used_digits:
                used_digits.append(temp)
                result = (result * 10) + temp
        return result        
        
    # Evaluates the bull, cow, and milk values for the given guess, assuming __validateGuess() returns True
    def evaluateGuess(self, guess):
        pass
    """
    def start_timer():
        pass
    """

"""
class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_code = db.Column(db.String(10), nullable=False, unique=True)

    def __init__(self, puzzle_code):
        self.puzzle_code = puzzle_code
    
    def generate_puzzle():
        pass

    def get_puzzle():
        pass
    
    def get_json(self):
        return {
            'id': self.id,
            'puzzle_code': self.puzzle_code
        }
"""