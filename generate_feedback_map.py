import os
import pickle
import argparse
from tqdm import tqdm

from funcs import split
from word_lists import WordListManager

# --- Helper function to get feedback (copied and adapted from rules.py) ---
def get_feedback(guess, solution):
    colors = split('bbbbb')
    guess_split = split(guess)
    solution_split = list(split(solution)) # Use a mutable copy

    # First pass: Check for green letters
    for i, letter in enumerate(guess_split):
        if letter == solution_split[i]:
            colors[i] = 'g'
            solution_split[i] = None  # Mark as used

    # Second pass: Check for yellow and black letters
    for i, letter in enumerate(guess_split):
        if colors[i] != 'g':  # Only check if not already marked green
            if letter in solution_split:
                colors[i] = 'y'
                solution_split[solution_split.index(letter)] = None  # Mark as used
            else:
                colors[i] = 'b'
    return "".join(colors)

def generate_and_save_feedback_map(feedback_map_cache_file="feedback_map.pkl"):
    print("Generating feedback map...")
    
    allowed_guesses = word_list_manager.get_allowed_guesses()
    possible_solutions = word_list_manager.get_possible_solutions()
    
    feedback_map = {}
    for guess in tqdm(allowed_guesses, desc="Pre-calculating feedback map"):
        for solution in possible_solutions:
            feedback_map[(guess, solution)] = get_feedback(guess, solution)
    
    print("Feedback map pre-calculation complete.")
    print(f"Saving feedback map to {feedback_map_cache_file}...")
    with open(feedback_map_cache_file, 'wb') as f:
        pickle.dump(feedback_map, f)
    print("Feedback map saved to cache.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and cache the Wordle feedback map.")
    parser.add_argument("--output_file", type=str, default="feedback_map.pkl",
                        help="Name of the output pickle file for the feedback map.")
    parser.add_argument("--full_list", action="store_true", default=False,
                        help="Use the full list of words instead of a subset.")
    parser.add_argument("--subset_size", type=int, default=100,
                        help="Size of the random subset to use.")
    parser.add_argument("--random_seed", type=int, default=None,
                        help="Random seed for subset generation. If not provided, a random seed will be generated.")
    args = parser.parse_args()

    # Re-initialize word_list_manager with the parsed arguments
    word_list_manager = WordListManager(args)

    generate_and_save_feedback_map(args.output_file)
