import numpy as np

from rules import game

# game format: 5 letter word followed by 5 letter string, each char in string contains 'b' or 'y' or 'g' for black or yellow or green respectively

words = np.genfromtxt('data/wordle_allowed_guesses_unsorted.txt', dtype=str)

# fix seed. seed 0 gives solution 'argle'
np.random.seed(seed=0)

index = np.random.randint(low=0, high=len(words), size=1, dtype=int)[0]

solution = words[index]

game = game(solution=solution)
tries = 0
guess = '-----'

while guess != solution:
    tries +=1
    guess = input('enter your next guess: ')
    print(game.enter(guess=guess))

print('you won! it took ' + str(tries) + ' guesses.')