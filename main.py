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
import word_lists
from visualizations import plot_guess_distribution

MAX_TRIES = 6
CHECKPOINT_INTERVAL = 10 # Save checkpoint every N solutions
CHECKPOINTS_DIR = "checkpoints"
SUBSET_SIZE = 100 # Define SUBSET_SIZE as a constant

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

def run_simulation(report_dir, search_depth=1, optimization_metric='min_avg_remaining', random_seed=None):
    start_time = time.time() # Start timer

    possible_solutions_subset = word_lists.get_possible_solutions()
    allowed_guesses_subset = word_lists.get_allowed_guesses()

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

    wordle_solver = solver(search_depth, optimization_metric)

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
            current_guess = wordle_solver.get_next_guess(guess_history)
            feedback = game_instance.enter(guess=current_guess)
            guess_history.append((current_guess, feedback))

            if "".join(feedback) == "ggggg":
                won = True
                results.append(tries)
                break
        
        if not won:
            failed_solutions.append(solution)
            results.append(MAX_TRIES + 1) # Mark as failed

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
    average_tries = sum(results) / total_games
    
    tries_distribution = collections.defaultdict(int)
    for t in results:
        tries_distribution[t] += 1

    report_content = f"""
--- Solver Performance Report ---
Total solutions simulated: {total_games}
"""
    subset_info = word_lists.get_subset_info()
    if subset_info["subset_mode"]:
        report_content += f"Used a subset of {subset_info['subset_size']} words for both solutions and guesses (Random Seed: {subset_info['random_seed']}).\n"
    report_content += f"Average guesses per game: {average_tries:.2f}\n\nGuess Distribution:\n"""
    for t in sorted(tries_distribution.keys()):
        if t <= MAX_TRIES:
            report_content += f"  {t} tries: {tries_distribution[t]} solutions\n"
        else:
            report_content += f"  Failed (>{MAX_TRIES} tries): {tries_distribution[t]} solutions\n"

    if failed_solutions:
        report_content += "\nSolutions that failed to be solved within 6 tries:\n"
        for sol in failed_solutions:
            report_content += f"- {sol}\n"
    else:
        report_content += "\nAll solutions were solved within 6 tries!\n"
    
    report_content += f"\nRuntime: {runtime:.2f} seconds\n"
    print(report_content)

    # --- Visualization ---
    plot_filename_base = f"guess_distribution_d{search_depth}_m{optimization_metric}"
    if subset_info["subset_mode"]:
        plot_filename_base += f"_subset_s{subset_info['random_seed']}"
    plot_filename = f"{plot_filename_base}.png"
    plot_guess_distribution(results, MAX_TRIES, search_depth, optimization_metric, subset_info["subset_mode"], average_tries, os.path.join(report_dir, plot_filename), random_seed=subset_info["random_seed"])

    return report_content, runtime, plot_filename

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a Wordle solver simulation.")
    parser.add_argument("--subset", action="store_true", help="Use a subset of words for testing.")
    parser.add_argument("--random_seed", type=int, default=None, help="Random seed for subset generation. If not provided, a random seed will be generated.")
    args = parser.parse_args()

    # If subset mode is enabled and no random seed is provided, generate one.
    if args.subset and args.random_seed is None:
        args.random_seed = random.randint(1, 1000) # Generate a random integer between 1 and 1000
        print(f"Generated random seed for subset: {args.random_seed}")

    word_lists.set_subset_params(args.subset, SUBSET_SIZE, args.random_seed)

    # Generate a unique directory name for this test run
    test_run_name = f"d1_mmin_avg_remaining"
    if args.subset:
        test_run_name += f"_subset_s{args.random_seed}"
    test_run_dir = os.path.join("test_reports", f"{test_run_name}")
    os.makedirs(test_run_dir, exist_ok=True)

    report_content, runtime, plot_filename = run_simulation(test_run_dir, search_depth=1, optimization_metric='min_avg_remaining', random_seed=args.random_seed)

    # Generate test report
    test_report_filename = os.path.join(test_run_dir, "test_report.md")
    with open(test_report_filename, "w") as f:
        f.write(f"# Test Report: Wordle Solver Simulation\n\n")
        f.write(f"## 1. What was done\n")
        subset_info = word_lists.get_subset_info()
        if subset_info["subset_mode"]:
            f.write(f"A simulation was run using the Wordle solver against a subset of {subset_info['subset_size']} words from the `wordle_answers.txt` list (Random Seed: {subset_info['random_seed']}). The set of allowed guesses was also limited to this same subset.\n\n")
        else:
            f.write(f"A simulation was run using the Wordle solver against the full list of possible solutions from the `wordle_answers.txt` list.\n\n")
        f.write(f"## 2. Why it was done\n")
        f.write(f"This test was performed to evaluate the performance of the Wordle solver.\n\n")
        f.write(f"## 3. What was specifically tested\n")
        f.write(f"The solver's performance was tested with the following configuration:\n")
        f.write(f"*   **Search Depth**: 1 (greedy approach)\n")
        f.write(f"*   **Optimization Metric**: `min_avg_remaining` (minimizing average remaining solutions)\n")
        if subset_info["subset_mode"]:
            f.write(f"*   **Dataset**: Subset of {subset_info['subset_size']} words from `wordle_answers.txt` for both solutions and allowed guesses (Random Seed: {subset_info['random_seed']}).\n\n")
        else:
            f.write(f"*   **Dataset**: Full list of allowed guesses and possible solutions.\n\n")
        f.write(f"## 4. Results\n")
        f.write(f"```\n{report_content}```\n\n")
        f.write(f"## 5. Guess Distribution Plot\n\n")
        f.write(f"![Guess Distribution]({plot_filename})\n\n")
        f.write(f"## 6. Runtime\n")
        f.write(f"The simulation completed in {runtime:.2f} seconds.\n")
    print(f"Test report saved to {test_report_filename}")
