from App.database import db
from sqlalchemy.orm import validates
from random import randint
from datetime import datetime, date

class Game(db.Model):
    # valid answers/guesses range from 0123 (4 digits, maintain the leading zero) to 9_876_543_210 (10 digits); all digits unique
    __MIN_ATTEMPTS = 5
    __MIN_CODE_LENGTH = 4
    __MAX_CODE_LENGTH = 10
    __MIN_CODE_VALUE = 123
    __MAX_CODE_VALUE = 9_876_543_210


    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date, nullable=False, unique=True, default=date.today)
    max_attempts = db.Column(db.Integer, db.Constraint(f"max_attempts >= {__MIN_ATTEMPTS}"), nullable=False)

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
        
        # If a specific answer is not provided, the answer is randomly generated
        #   using the provided answer length which MUST be provided.
        else:
            if answer_length is None:
                raise ValueError("MUST provide an answer length for random generation if not providing a specific answer")
            self.answer = self.generateAnswer(answer_length)

        self.answer_length = len(self.answer)

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
        if value < self.__MIN_ATTEMPTS:
            raise ValueError(f"expected max_attempts to have a minimum value of {self.__MIN_ATTEMPTS}; recieved {value}")
        return value

    @validates("answer")
    def validate_answer(self, key, value):
        try:
            value = int(value)    # Attempt to cast to int to ensure no non-numerical characters
        except ValueError:
            raise ValueError(f"could not cast answer of type <{value.__class__.__name__}> to type int")
        
        if not self.__MIN_CODE_VALUE <= value <= self.__MAX_CODE_VALUE:
            raise ValueError(f"expected answer to be within the range {self.__MIN_CODE_VALUE:0{self.__MIN_CODE_LENGTH}d} to {self.__MAX_CODE_VALUE}, inclusive; recieved <{value}>")
        return value
    
    @validates("answer_length")
    def validate_answer_length(self, key, value):
        if not self.__MIN_CODE_VALUE <= value <= self.__MAX_CODE_VALUE:
            raise ValueError(f"expected answer length to be within the range {self.__MIN_CODE_VALUE:0{self.__MIN_CODE_LENGTH}d} to {self.__MAX_CODE_VALUE} digits, inclusive; recieved <{value}> digits")
        return value
    
    def generate_answer(self, answer_length):
        try:
            answer_length = int(answer_length)    # Attempt to cast to int to ensure no non-numerical characters
        except ValueError:
            raise ValueError(f"could not cast answer length of type <{answer_length.__class__.__name__}> to type int")
        
        if not (self.__MIN_CODE_LENGTH <= answer_length <= self.__MAX_CODE_LENGTH):
            raise ValueError(f"expected answer length to be within {self.__MIN_CODE_LENGTH} and {self.__MAX_CODE_LENGTH} digits, inclusive; recieved <{answer_length}> digits")
        
        used_digits = []
        result = 0
        
        while len(result) < answer_length:
            temp = randint(0, 9)
            if temp not in used_digits:
                used_digits.append(temp)
                result = (result * 10) + temp
        return result        
    
    # Raises a ValueError if the guess fails any of the constraints, otherwise returns True
    def __validateGuess(self, guess):
        try:
            # Attempt to cast the guess to an integer to ensure it's a valid numbedr
            guess = int(guess)

        except ValueError:
            # Raise an error if the guess cannot be converted to an integer
            raise ValueError(f"guess of type {guess.__class__.__name__} could not be cast to type int")
        
        # Convert guess to a string to count its digits
        guess_str = str(guess)
        guess_length = len(guess_str)

        # Check if the guess length is the same as the answer length
        if guess_length != self.answer_length:
            raise ValueError(f"expected length of guess to be equal {self.answer_length} digits; recieved {guess_length} digits; )")
        
        # Check if the guess value is within the valid range
        if not (self.__MIN_CODE_VALUE <= guess <= self.__MAX_CODE_VALUE):
            raise ValueError(f"expected guess to be within {self.__MIN_CODE_VALUE:0{self.__MIN_CODE_LENGTH}d} and {self.__MAX_CODE_VALUE}, inclusive; recieved <{guess}>)")
        
        # Check if all digits in the guess are unique
        used_digits = set()
        for digit in guess_str:
            if digit in used_digits:
                raise ValueError(f"expected each digit of the guess <{guess}> to be unique")
            used_digits.add(digit)
    
        # Returns True if all the validation checks pass
        return True       
        
    # Evaluates the bull, cow, and milk values for the given guess, assuming __validateGuess() returns True,
    #   returning their values in a tuple
    # If __validateGuess() raises a ValueError, the error is passed up to the calling function for handling
    def evaluateGuess(self, guess):
        results = {
            "bulls" : 0,
            "cows" : 0,
            "milk" : 0,
        }

        try:
            if (self.__validateGuess(guess)):
                guess = str(guess)
                ans_str = str(self.answer)

                for g, a in zip(guess, ans_str):
                    if g == a:
                        results["bulls"] += 1
                    elif g in ans_str:
                        results["cows"] += 1

                results["milk"] = len(ans_str) - results["bulls"] - results["cows"]
                return results
            
        except ValueError as e:
            raise e
