import random

_SUBSET_MODE = False
_SUBSET_SIZE = 100
_RANDOM_SEED = None

_allowed_guesses = None
_possible_solutions = None
_random_subset = None

def _load_word_lists():
    global _allowed_guesses, _possible_solutions, _random_subset
    with open('data/wordle_allowed_guesses.txt', 'r') as f:
        _allowed_guesses = f.read().splitlines()
    with open('data/wordle_answers.txt', 'r') as f:
        _possible_solutions = f.read().splitlines()
    
    if _RANDOM_SEED is not None:
        random.seed(_RANDOM_SEED)
    _random_subset = random.sample(_possible_solutions, _SUBSET_SIZE)

def set_subset_params(subset_mode, subset_size, random_seed):
    global _SUBSET_MODE, _SUBSET_SIZE, _RANDOM_SEED, _allowed_guesses, _possible_solutions, _random_subset
    _SUBSET_MODE = subset_mode
    _SUBSET_SIZE = subset_size
    _RANDOM_SEED = random_seed
    # Reload word lists if parameters change or if not loaded yet
    _load_word_lists()

def get_allowed_guesses():
    if _allowed_guesses is None: # Initial load if set_subset_params wasn't called first
        _load_word_lists()
    if _SUBSET_MODE:
        return _random_subset
    return _allowed_guesses

def get_possible_solutions():
    if _possible_solutions is None: # Initial load if set_subset_params wasn't called first
        _load_word_lists()
    if _SUBSET_MODE:
        return _random_subset
    return _possible_solutions

def get_subset_info():
    return {
        "subset_mode": _SUBSET_MODE,
        "subset_size": _SUBSET_SIZE,
        "random_seed": _RANDOM_SEED
    }
