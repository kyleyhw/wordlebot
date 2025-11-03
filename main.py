import random
import collections
import matplotlib.pyplot as plt
import os
from tqdm import tqdm # Import tqdm

from rules import game
from solver import solver, get_feedback

# Load word lists
with open('data/wordle_allowed_guesses.txt', 'r') as f:
    allowed_guesses_list = f.read().splitlines()

with open('data/wordle_answers.txt', 'r') as f:
    possible_solutions_list = f.read().splitlines()

MAX_TRIES = 6

def plot_guess_distribution(results, max_tries, output_filename="guess_distribution.png"):
    distribution = collections.defaultdict(int)
    for t in results:
        if t <= max_tries:
            distribution[t] += 1
        else:
            distribution[f">{max_tries}"] += 1

    labels = [str(i) for i in range(1, max_tries + 1)]
    if f">{max_tries}" in distribution:
        labels.append(f">{max_tries}")
    
    counts = [distribution[int(label)] if label.isdigit() else distribution[label] for label in labels]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel("Number of Guesses")
    plt.ylabel("Number of Solutions")
    plt.title("Wordle Solver Guess Distribution")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(output_filename)
    plt.close()
    print(f"Guess distribution plot saved to {output_filename}")

def run_simulation(search_depth=1, optimization_metric='min_avg_remaining'):
    wordle_solver = solver(allowed_guesses_list, possible_solutions_list, search_depth, optimization_metric)

    results = [] # Stores number of tries for each solution
    failed_solutions = []

    print("\nStarting simulations...")
    # Wrap the loop with tqdm for a progress bar
    for solution in tqdm(possible_solutions_list, desc="Simulating Wordle Solutions"):
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

    print("\nSimulations complete!")
    
    # --- Analysis and Reporting ---
    total_games = len(results)
    average_tries = sum(results) / total_games
    
    tries_distribution = collections.defaultdict(int)
    for t in results:
        tries_distribution[t] += 1

    print("\n--- Solver Performance Report ---")
    print(f"Total solutions simulated: {total_games}")
    print(f"Average guesses per game: {average_tries:.2f}")
    print("\nGuess Distribution:")
    for t in sorted(tries_distribution.keys()):
        if t <= MAX_TRIES:
            print(f"  {t} tries: {tries_distribution[t]} solutions")
        else:
            print(f"  Failed (>{MAX_TRIES} tries): {tries_distribution[t]} solutions")

    if failed_solutions:
        print("\nSolutions that failed to be solved within 6 tries:")
        for sol in failed_solutions:
            print(f"- {sol}")
    else:
        print("\nAll solutions were solved within 6 tries!\n")

    # --- Visualization ---
    plot_guess_distribution(results, MAX_TRIES, os.path.join("docs", "guess_distribution.png"))

if __name__ == "__main__":
    # Run simulation with least computationally expensive options
    run_simulation(search_depth=1, optimization_metric='min_avg_remaining')