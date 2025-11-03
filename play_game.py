import numpy as np
import random
import sys

from rules import game

# Load word lists
with open('data/wordle_allowed_guesses.txt', 'r') as f:
    allowed_guesses = set(f.read().splitlines())

with open('data/wordle_answers.txt', 'r') as f:
    possible_solutions = f.read().splitlines()

MAX_TRIES = 6

def display_board(guess_history, tries_left):
    print("\n" + "="*30)
    print(f"Tries Left: {tries_left}")
    print("="*30)
    for guess_word, feedback_colors in guess_history:
        display_line = []
        for i, char in enumerate(guess_word):
            color = feedback_colors[i]
            if color == 'g':
                display_line.append(f"[{char.upper()}]") # Green
            elif color == 'y':
                display_line.append(f"({char.upper()})") # Yellow
            else:
                display_line.append(f" {char.upper()} ") # Black
        print(" ".join(display_line))
    for _ in range(tries_left):
        print(" _  _  _  _  _ ")
    print("="*30)

def play_wordle():
    solution = random.choice(possible_solutions)
    game_instance = game(solution=solution)
    guess_history = []
    tries = 0

    print("Welcome to Wordle!")
    print(f"The solution is: {solution}") # For debugging, remove later

    while tries < MAX_TRIES:
        display_board(guess_history, MAX_TRIES - tries)

        guess = input("Enter your 5-letter guess: ").lower()

        if len(guess) != 5:
            print("Invalid guess: Must be 5 letters long.")
            continue
        if not guess.isalpha():
            print("Invalid guess: Must contain only letters.")
            continue
        if guess not in allowed_guesses:
            print("Invalid guess: Not in word list.")
            continue

        tries += 1
        feedback = game_instance.enter(guess=guess)
        guess_history.append((guess, feedback))

        if "".join(feedback) == "ggggg":
            display_board(guess_history, MAX_TRIES - tries)
            print(f"Congratulations! You guessed the word '{solution}' in {tries} tries.")
            return

    display_board(guess_history, 0)
    print(f"Game Over! You ran out of tries. The word was '{solution}'.")

if __name__ == "__main__":
    play_wordle()
