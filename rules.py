import numpy as np
import collections

from funcs import merge, split

words = np.genfromtxt('data/wordle_allowed_guesses_unsorted.txt', dtype=str)

# game format: 5 letter word followed by 5 letter string, each char in string contains 'b' or 'y' or 'g' for black or yellow or green respectively

class game:
    def __init__(self, solution):
        self.solution = split(solution)

    def turn(self, guess):
        string = split('bbbbb')

        guess = split(guess)

        for i, letter in enumerate(guess):
            if letter == self.solution[i]:
                string[i] = 'g'
            elif letter in self.solution:
                if collections.Counter(self.solution)[letter] > collections.Counter(checked_letters)[letter]:
                    string[i] = 'y'
            checked_letters = guess[:i]
            print(checked_letters)
        return string

test_game = game('aaaba')
test_guess = test_game.turn('aazbz')

print(test_guess)