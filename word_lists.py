import random
import argparse

DEFAULT_USE_FULL_LIST = False # Set to True to use the full list by default, False to use subset by default

class WordListManager:
    def __init__(self, args=None):
        if args is None:
            # Default behavior when no argparse arguments are provided
            self.subset_mode = not DEFAULT_USE_FULL_LIST
            self.subset_size = 100
            self.random_seed = random.randint(1, 1000) # Generate a random seed by default
            print(f"WordListManager: Initialized with default subset mode (size={self.subset_size}, seed={self.random_seed}).")
        else:
            # Use argparse arguments
            self.subset_mode = not args.full_list
            self.subset_size = args.subset_size if hasattr(args, 'subset_size') else 100
            self.random_seed = args.random_seed

            if self.subset_mode and self.random_seed is None:
                self.random_seed = random.randint(1, 1000)
                print(f"WordListManager: Generated random seed for subset: {self.random_seed}")
            
            print(f"WordListManager: Initialized with subset_mode={self.subset_mode}, subset_size={self.subset_size}, random_seed={self.random_seed}.")

        self.allowed_guesses = None
        self.possible_solutions = None
        self.random_subset = None
        self._load_word_lists()

    def _load_word_lists(self):
        with open('data/wordle_allowed_guesses.txt', 'r') as f:
            self.allowed_guesses = f.read().splitlines()
        with open('data/wordle_answers.txt', 'r') as f:
            self.possible_solutions = f.read().splitlines()
        
        if self.subset_mode:
            if self.random_seed is not None:
                random.seed(self.random_seed)
            self.random_subset = random.sample(self.possible_solutions, self.subset_size)
            print(f"WordListManager: Loaded a random subset of {self.subset_size} words (seed={self.random_seed}).")
        else:
            print("WordListManager: Loaded full word lists.")

    def get_allowed_guesses(self):
        if self.subset_mode:
            return self.random_subset
        return self.allowed_guesses

    def get_possible_solutions(self):
        if self.subset_mode:
            return self.random_subset
        return self.possible_solutions

    def get_subset_info(self):
        return {
            "subset_mode": self.subset_mode,
            "subset_size": self.subset_size,
            "random_seed": self.random_seed
        }

# Create a global instance of WordListManager
# This will be imported by other modules
# If word_lists.py is run directly, it will parse its own args
# Otherwise, it will initialize with default subset mode
_parser = argparse.ArgumentParser(add_help=False) # add_help=False to prevent conflicts with main parsers
_parser.add_argument("--full_list", action="store_true", default=False,
                    help="Use the full list of words instead of a subset.")
_parser.add_argument("--subset_size", type=int, default=100,
                    help="Size of the random subset to use.")
_parser.add_argument("--random_seed", type=int, default=None,
                    help="Random seed for subset generation. If not provided, a random seed will be generated.")

# Try to parse known arguments. This allows other scripts to parse their own arguments
# without word_lists.py complaining about unknown arguments.
_args, _ = _parser.parse_known_args()

word_list_manager = WordListManager(_args)