import random
import collections
import os
from tqdm import tqdm # Import tqdm
import time # Import time for runtime measurement
import json # Import json for checkpointing
import argparse
import sys # Import sys for maxsize

from rules import game
from solver import solver, get_feedback
from word_lists import WordListManager
from visualizations import plot_guess_distribution

MAX_TRIES = 6
CHECKPOINT_INTERVAL = 10 # Save checkpoint every N solutions
CHECKPOINTS_DIR = "checkpoints"

def save_checkpoint(checkpoint_data, filename):
    os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
    filepath = os.path.join(CHECKPOINTS_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(checkpoint_data, f)
    print(f"Checkpoint saved to {filepath}")

def load_checkpoint(filename):
    filepath = os.path.join(CHECKPOINTS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            checkpoint_data = json.load(f)
        print(f"Checkpoint loaded from {filepath}")
        return checkpoint_data
    return None

def run_simulation(word_list_manager_instance, report_dir, search_depth=1, optimization_metric='min_avg_remaining', random_seed=None):
    start_time = time.time() # Start timer

    possible_solutions_subset = word_list_manager_instance.get_possible_solutions()
    allowed_guesses_subset = word_list_manager_instance.get_allowed_guesses()

    # Generate unique checkpoint filename
    checkpoint_filename = f"checkpoint_d{search_depth}_m{optimization_metric}"
    if random_seed is not None:
        checkpoint_filename += f"_s{random_seed}"
    checkpoint_filename += ".json"
    
    # Try to load checkpoint
    checkpoint_data = load_checkpoint(checkpoint_filename)

    if checkpoint_data:
        results = checkpoint_data['results']
        failed_solutions = checkpoint_data['failed_solutions']
        start_index = checkpoint_data['last_solution_index'] + 1
        print(f"Resuming simulation from solution index {start_index}")
    else:
        results = []
        failed_solutions = []
        start_index = 0

    wordle_solver = solver(word_list_manager_instance, search_depth, optimization_metric)

    print("\nStarting simulations...")
    # Wrap the loop with tqdm for a progress bar
    # Use initial=start_index to correctly display progress from checkpoint
    for i in tqdm(range(start_index, len(possible_solutions_subset)), initial=start_index, total=len(possible_solutions_subset), desc="Simulating Wordle Solutions"):
        solution = possible_solutions_subset[i]
        game_instance = game(solution=solution)
        guess_history = []
        tries = 0
        won = False

        while tries < MAX_TRIES:
            tries += 1
            current_guess_recommendations = wordle_solver.get_next_guess(guess_history)
            current_guess = current_guess_recommendations[0][0] # Take the best guess (first in the list)
            feedback = game_instance.enter(guess=current_guess)
            guess_history.append((current_guess, feedback))

            if feedback == "ggggg":
                won = True
                game_result = {
                    'solution': solution,
                    'tries': tries,
                    'won': won,
                    'guess_history': guess_history
                }
                results.append(game_result)
                break
        
        if not won:
            failed_solutions.append(solution)
            game_result = {
                'solution': solution,
                'tries': MAX_TRIES + 1,
                'won': won,
                'guess_history': guess_history
            }
            results.append(game_result)

        # Save checkpoint periodically
        if (i + 1) % CHECKPOINT_INTERVAL == 0 or (i + 1) == len(possible_solutions_subset):
            checkpoint_data = {
                'results': results,
                'failed_solutions': failed_solutions,
                'last_solution_index': i
            }
            save_checkpoint(checkpoint_data, checkpoint_filename)

    end_time = time.time() # End timer
    runtime = end_time - start_time

    print("\nSimulations complete!")
    
    # --- Analysis and Reporting ---
    total_games = len(results)
    # Extract tries from the new results structure
    all_tries = [game_result['tries'] for game_result in results]
    average_tries = sum(all_tries) / total_games
    
    tries_distribution = collections.defaultdict(int)
    for t in all_tries:
        tries_distribution[t] += 1

    report_content = f"""
--- Solver Performance Report ---
Total solutions simulated: {total_games}
"""
    subset_info = word_list_manager_instance.get_subset_info()
    if subset_info["subset_mode"]:
        report_content += f"Used a subset of {subset_info['subset_size']} words for both solutions and guesses (Random Seed: {subset_info['random_seed']}).\n"
    report_content += f"Average guesses per game: {average_tries:.2f}\n\nGuess Distribution:\n"""
    for t in sorted(tries_distribution.keys()):
        if t <= MAX_TRIES:
            report_content += f"  {t} tries: {tries_distribution[t]} solutions\n"
        else:
            report_content += f"  Failed (>{MAX_TRIES} tries): {tries_distribution[t]} solutions\n"

    report_content += "\n--- Game Details ---\n"
    for game_result in results:
        solution = game_result['solution']
        tries = game_result['tries']
        won = game_result['won']
        guess_history = game_result['guess_history']

        status = "Won" if won else "Failed"
        report_content += f"\nSolution: {solution.upper()} ({status} in {tries} tries)\n"
        for i, (guess, feedback) in enumerate(guess_history):
            report_content += f"  {i+1}. {guess.upper()} -> {feedback}\n"

    if failed_solutions:
        report_content += "\nSolutions that failed to be solved within 6 tries:\n"
        for sol in failed_solutions:
            report_content += f"- {sol}\n"
    else:
        report_content += "\nAll solutions were solved within 6 tries!\n"
    
    report_content += f"\nRuntime: {runtime:.2f} seconds\n"
    print(report_content)

    # Save the report content to a markdown file
    report_filepath = os.path.join(report_dir, f"report_{test_run_name}.md")
    with open(report_filepath, 'w') as f:
        f.write(report_content)
    print(f"Report saved to {report_filepath}")

    # --- Visualization ---
    plot_filename_base = f"guess_distribution_d{search_depth}_m{optimization_metric}"
    if subset_info["subset_mode"]:
        plot_filename_base += f"_subset_s{subset_info['random_seed']}"
    plot_filename = f"{plot_filename_base}.png"
    plot_guess_distribution(results, MAX_TRIES, search_depth, optimization_metric, subset_info["subset_mode"], average_tries, os.path.join(report_dir, plot_filename), random_seed=subset_info["random_seed"])

    return report_content, runtime, plot_filename, checkpoint_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Wordle solver simulation.")
    parser.add_argument("--search_depth", type=int, default=1, help="Search depth for the solver.")
    parser.add_argument("--optimization_metric", type=str, default="min_avg_remaining",
                        choices=["min_max_remaining", "min_avg_remaining", "min_avg_guesses"],
                        help="Optimization metric for the solver.")
    parser.add_argument("--full_list", action="store_true", default=False,
                        help="Use the full list of words instead of a subset.")
    parser.add_argument("--subset_size", type=int, default=100,
                        help="Size of the random subset to use.")
    parser.add_argument("--random_seed", type=int, default=None,
                        help="Random seed for subset generation. If not provided, a random seed will be generated.")
    args = parser.parse_args()

    # Re-initialize word_list_manager with the parsed arguments
    from word_lists import WordListManager
    word_list_manager = WordListManager(args)

    # Generate a unique directory name for this test run
    test_run_name = f"d{args.search_depth}_m{args.optimization_metric}"
    subset_info = word_list_manager.get_subset_info()
    if subset_info["subset_mode"]:
        test_run_name += f"_subset_s{subset_info['random_seed']}"
    test_run_dir = os.path.join("test_reports", f"{test_run_name}")
    os.makedirs(test_run_dir, exist_ok=True)

    report_content, runtime, plot_filename, checkpoint_filename = run_simulation(word_list_manager, test_run_dir, search_depth=args.search_depth, optimization_metric=args.optimization_metric, random_seed=subset_info['random_seed'])

    # Delete the checkpoint file after the simulation is complete and reports are saved
    checkpoint_filepath = os.path.join(CHECKPOINTS_DIR, checkpoint_filename)
    if os.path.exists(checkpoint_filepath):
        os.remove(checkpoint_filepath)
        print(f"Checkpoint file {checkpoint_filepath} deleted.")
