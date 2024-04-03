from random import randint

MIN_CODE_LENGTH = 3
MAX_CODE_LENGTH = 10
NUM_GUESSES = 6

class Guess:
    def __init__(self, guess, code):
        self.__guess = None
        self.__code = None
        self.__bulls = None
        self.__cows = None
        self.__milk = None

        self.updateCode(code)
        self.updateGuess(guess)

    
    # Returns true if the guess and code provided are not empty, not None,
    #   are within the length requirements, and are the same length
    def checkParams(self):
        return (
            self.__guess != "" and self.__guess is not None
            and self.__code != "" and self.__code is not None
            and len(self.__guess) >= MIN_CODE_LENGTH and len(self.__guess) <= MAX_CODE_LENGTH
            and len(self.__code) >= MIN_CODE_LENGTH and len(self.__code) <= MAX_CODE_LENGTH
            and len(self.__guess) == len(self.__code)
        )


    # Returns True if the guess and code are neither empty nor None, and if bulls, cows,
    #   and milk are neither -1 (meaning a calculation failed) nor None (meaning the
    #   initial value has somehow not been updated)
    # Returns False otherwise
    def isValid(self):
        return (
            self.checkParams()
            and self.__bulls != -1 and self.__bulls is not None
            and self.__cows != -1 and self.__cows is not None
            and self.__milk != -1 and self.__milk is not None
            )
    
    # Calculates the bulls (number of correct characters in the correct position for the given code)
    # Returns True if the calculation is successful and False if it fails
    def calc_bulls(self):
        if not self.checkParams():
            self.__bulls = -1
            self.__cows = -1
            self.__milk = -1
            return False
        
        self.__bulls = 0
        for g, c in zip(self.__guess, self.__code):
            if g == c:
                self.__bulls += 1
        return True


    # Calculates the cows (number of correct characters in the guess with incorrect positions
    #     for the given code)
    # Returns True if the calculation is successful and False if it fails
    def calc_cows(self):
        if not self.checkParams():
            self.__bulls = -1
            self.__cows = -1
            self.__milk = -1
            return False
        
        self.__cows = 0
        for g, c in zip(self.__guess, self.__code):
            if g in self.__code and g != c:
                self.__cows += 1
        return True

    # Calculates the milk (number of incorrect characters in the guess for the given code)
    # Returns True if the calculation is successful and False if it fails
    def calc_milk(self):
        if not self.checkParams():
            self.__bulls = -1
            self.__cows = -1
            self.__milk = -1
            return False
        
        self.__milk = len(self.__guess) - self.__bulls - self.__cows
        return True
    
    def getGuess(self):
        return self.__guess
    
    def getCode(self):
        return self.__code
    
    def getBulls(self):
        return self.__bulls
    
    def getCows(self):
        return self.__cows
    
    def getMilk(self):
        return self.__milk
    
    def updateGuess(self, newGuess):
        self.__guess = str(newGuess)
        self.calc_bulls()
        self.calc_cows()
        self.calc_milk()

    def updateCode(self, newCode):
        self.__code = str(newCode)
        self.calc_bulls()
        self.calc_cows()
        self.calc_milk()

    # Returns False if isValid() does or if the any of the digits in the guess repeat
    # Returns True if the above is not met and the guess is the same length as the code
    def evaluateGuess(self):
        if not self.isValid():
            print("[ERROR: Guess invalid.]\n")
            return -1
        
        used_digits = []
        for c in self.__guess:
            if c in used_digits:
                print(f"Found repeat digit - {c}")
                return False
            used_digits.append(c)
        return 0 if self.__bulls == len(self.__code) and self.__bulls != 0 else 1


# Global code generator function; each character is unique
def generate_code(code_length):
    try:
        code_length = int(code_length)
    except ValueError as e:
        print(e)
        return None
    
    # There are only 10 Arabic numerals, i.e., 0-9
    if code_length < MIN_CODE_LENGTH or code_length > MAX_CODE_LENGTH:
        return None
    
    used_digits = []
    code = ""
    
    while len(code) < code_length:
        temp = randint(0, 9)
        if temp not in used_digits:
            used_digits.append(temp)
            code += str(temp)
    return code


if __name__ == "__main__":
    code_length = ""
    try:
        code_length = int(input(f"Select a code length (max: {MAX_CODE_LENGTH}, min: {MIN_CODE_LENGTH}): "))
    except ValueError:
        print("[ERROR: Expected an integer.]\n")
        exit(1)
    else:
        if code_length < MIN_CODE_LENGTH or code_length > MAX_CODE_LENGTH:
            print("[ERROR: Invalid value.]\n")
            exit(1)
    
    code = generate_code(code_length)
    if code is None:
        print("[ERROR: Could not generate code.]\n")
        exit(1)
    
    userGuess = Guess(None, code)
    for currGuess in range(NUM_GUESSES):
        print(f"Attempt {currGuess + 1}/{NUM_GUESSES}:")
        userGuess.updateGuess(input(f"Guess the generated code (expecting {code_length} unique digits): "))
        guessEvaluation = userGuess.evaluateGuess()
        
        match(guessEvaluation):
            case -1:
                continue

            case 1:
                print("Incorrect\n")
                
            case 0:
                print("Correct")
                break
                
            case _:
                print("[ERROR: An unexpected error has occurred. Terminating program...]")
                exit(1)

        print(f"Bulls: {userGuess.getBulls()}")
        print(f"Cows: {userGuess.getCows()}")
        print(f"Milk: {userGuess.getMilk()}\n")

    print(f"\n\nAnswer: {code}")
