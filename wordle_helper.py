import argparse
import sys
import collections

from solver import solver
from funcs import split # Assuming split is needed for feedback parsing
from word_lists import word_list_manager

def get_feedback_from_user():
    while True:
        feedback_str = input("Enter feedback (e.g., 'bybyb' for black, yellow, black, yellow, black): ").lower()
        if len(feedback_str) == 5 and all(c in ['b', 'y', 'g'] for c in feedback_str):
            return feedback_str
        else:
            print("Invalid feedback. Please use 'b', 'y', or 'g' for each of the 5 letters.")

def display_guess_history(guess_history):
    if not guess_history:
        print("\nNo guesses yet.")
        return
    print("\n--- Current Game State ---")
    for i, (guess_word, feedback_colors) in enumerate(guess_history):
        display_line = []
        for j, char in enumerate(guess_word):
            color = feedback_colors[j]
            if color == 'g':
                display_line.append(f"[{char.upper()}]") # Green
            elif color == 'y':
                display_line.append(f"({char.upper()})") # Yellow
            else:
                display_line.append(f" {char.upper()} ") # Black
        print(f"Guess {i+1}: {' '.join(display_line)}")
    print("--------------------------")

def main():
    parser = argparse.ArgumentParser(description="Interactive Wordle Helper to suggest the best next guess.")
    parser.add_argument("--depth", type=int, default=1,
                        help="Search depth for the solver (e.g., 1 for greedy, 2 for looking ahead).")
    parser.add_argument("--metric", type=str, default="min_avg_remaining",
                        choices=["min_max_remaining", "min_avg_remaining", "min_avg_guesses"],
                        help="Optimization metric for the solver.")
    args = parser.parse_args()

    if word_list_manager.get_subset_info()["subset_mode"]:
        print("--- Running in Subset Mode ---")

    print(f"Initializing Wordle solver with depth={args.depth}, metric={args.metric}...")
    wordle_solver = solver(search_depth=args.depth, optimization_metric=args.metric)
    print("Solver initialized. Let's play!")

    guess_history = [] # List of (guess_word, feedback_str) tuples

    while True:
        display_guess_history(guess_history)

        if not guess_history:
            # First guess, use the pre-calculated best initial guess
            next_guess = wordle_solver.get_next_guess(guess_history)
            print(f"Recommended first guess: {next_guess.upper()}")
        else:
            # Subsequent guesses, prompt for previous guess and feedback
            last_guess = input("Enter your last guess (5 letters): ").lower()
            if len(last_guess) != 5 or not last_guess.isalpha():
                print("Invalid guess. Please enter a 5-letter word.")
                continue
            feedback = get_feedback_from_user()
            guess_history.append((last_guess, feedback))

            if feedback == "ggggg":
                print(f"Congratulations! You solved it in {len(guess_history)} guesses.")
                break

            next_guess = wordle_solver.get_next_guess(guess_history)
            print(f"Recommended next guess: {next_guess.upper()}")
        
        play_again = input("\nPress Enter to continue for the next guess, or type 'q' to quit: ").lower()
        if play_again == 'q':
            break

    print("Thank you for using the Wordle Helper!")

if __name__ == "__main__":
    main()
