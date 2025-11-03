import random

SUBSET_MODE = False
SUBSET_SIZE = 100

_allowed_guesses = None
_possible_solutions = None

def _load_word_lists():
    global _allowed_guesses, _possible_solutions
    with open('data/wordle_allowed_guesses.txt', 'r') as f:
        _allowed_guesses = f.read().splitlines()
    with open('data/wordle_answers.txt', 'r') as f:
        _possible_solutions = f.read().splitlines()

def get_allowed_guesses():
    if _allowed_guesses is None:
        _load_word_lists()
    if SUBSET_MODE:
        return _possible_solutions[:SUBSET_SIZE]
    return _allowed_guesses

def get_possible_solutions():
    if _possible_solutions is None:
        _load_word_lists()
    if SUBSET_MODE:
        return _possible_solutions[:SUBSET_SIZE]
    return _possible_solutions
