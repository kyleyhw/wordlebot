import numpy as np

from funcs import split, count_occurrences

words = np.genfromtxt('data/wordle_allowed_guesses_unsorted.txt', dtype=str)

# game format: 5 letter word followed by 5 letter string, each char in string contains 'b' or 'y' or 'g' for black or yellow or green respectively

class game:
    def __init__(self, solution):
        self.solution = split(solution)

    def enter(self, guess):
        colors = split('bbbbb')
        guess = split(guess)
        green_letters = []
        for i, letter in enumerate(guess):
            if letter == self.solution[i]:
                colors[i] = 'g'
                green_letters.append(letter)

        for i, letter in enumerate(guess):
            checked_letters = guess[:i]
            if letter in self.solution and \
                    colors[i] != 'g' and \
                    count_occurrences(letter, self.solution) >= \
                    (count_occurrences(letter, green_letters) + count_occurrences(letter, checked_letters)):
            # the = in the >= is because checked_letters includes the current letter, for more elegant initialization
                colors[i] = 'y'
        return colors

test_game = game('prose')
print(test_game.enter('crane'))
print(test_game.enter('soily'))
print(test_game.enter('prose'))
