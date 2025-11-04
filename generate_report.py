import os
import collections
import matplotlib.pyplot as plt
from visualizations import plot_guess_distribution

MAX_TRIES = 6 # Assuming MAX_TRIES is a global constant or passed as argument

def generate_test_report(results, MAX_TRIES, search_depth, optimization_metric, subset_info, average_tries, report_dir, runtime, possible_solutions_subset, allowed_guesses_subset, wordle_solver):
    total_games = len(results)
    
    all_tries = [game_result['tries'] for game_result in results]
    
    tries_distribution = collections.defaultdict(int)
    for t in all_tries:
        if t <= MAX_TRIES:
            tries_distribution[t] += 1
        else:
            tries_distribution[f">{MAX_TRIES}"] += 1

    # --- Visualization ---
    plot_filename_base = f"guess_distribution_d{search_depth}_m{optimization_metric}"
    if subset_info["subset_mode"]:
        plot_filename_base += f"_subset_s{subset_info['random_seed']}"
    plot_filename = f"{plot_filename_base}.png"

    plot_guess_distribution(results, MAX_TRIES, search_depth, optimization_metric, subset_info["subset_mode"], average_tries, os.path.join(report_dir, plot_filename), random_seed=subset_info["random_seed"])
    print(f"Guess distribution plot saved to {os.path.join(report_dir, plot_filename)}")

    report_content = f"""
--- Solver Performance Report ---
Total solutions simulated: {total_games}
"""
    if subset_info["subset_mode"]:
        report_content += f"Used a subset of {subset_info['subset_size']} words for both solutions and guesses (Random Seed: {subset_info['random_seed']}).\n"
    report_content += f"Average guesses per game: {average_tries:.2f}\n\n"

    # Add best initial guess and its score
    best_initial_guess_data = wordle_solver.best_initial_guesses_by_config[(search_depth, optimization_metric)][0]
    report_content += f"Overall Best Initial Guess: {best_initial_guess_data[0].upper()} (Score: {best_initial_guess_data[1]:.2f})\n\n"

    # Embed the plot
    report_content += f"![Guess Distribution Plot]({plot_filename})\n\n"

    report_content += "Guess Distribution:\n"
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

    # Add list of possible solutions
    report_content += "\n### Possible Solutions Used (Subset):\n"
    report_content += ", ".join([s.upper() for s in possible_solutions_subset]) + "\n\n"

    # Add list of allowed guesses
    report_content += "\n### Allowed Guesses Used (Subset):\n"
    report_content += ", ".join([g.upper() for g in allowed_guesses_subset]) + "\n\n"

    report_content += f"\nRuntime: {runtime:.2f} seconds\n"
    
    # Save the report content to a markdown file
    test_run_name = f"d{search_depth}_m{optimization_metric}"
    if subset_info["subset_mode"]:
        test_run_name += f"_subset_s{subset_info['random_seed']}"
    report_filepath = os.path.join(report_dir, f"report_{test_run_name}.md")
    with open(report_filepath, 'w') as f:
        f.write(report_content)

