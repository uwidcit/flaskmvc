# valid answers/guesses range from 0123 (4 unique digits) to 9_876_543_210 (10 unique digits)
MIN_CODE_VALUE = 123    # Python doesnt allow integers to store leading zeroes directly
MAX_CODE_VALUE = 9_876_543_210
MIN_CODE_LENGTH = len(str(MIN_CODE_VALUE)) + 1    # Add 1 for leading 0
MAX_CODE_LENGTH = len(str(MAX_CODE_VALUE))