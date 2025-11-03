import random

SUBSET_MODE = False
SUBSET_SIZE = 100

_allowed_guesses = None
_possible_solutions = None
_random_subset = None

def _load_word_lists():
    global _allowed_guesses, _possible_solutions, _random_subset
    with open('data/wordle_allowed_guesses.txt', 'r') as f:
        _allowed_guesses = f.read().splitlines()
    with open('data/wordle_answers.txt', 'r') as f:
        _possible_solutions = f.read().splitlines()
    _random_subset = random.sample(_possible_solutions, SUBSET_SIZE)

def get_allowed_guesses():
    if _allowed_guesses is None:
        _load_word_lists()
    if SUBSET_MODE:
        return _random_subset
    return _allowed_guesses

def get_possible_solutions():
    if _possible_solutions is None:
        _load_word_lists()
    if SUBSET_MODE:
        return _random_subset
    return _possible_solutions
