import tkinter as tk
import matplotlib.pyplot as plt
import collections
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_feedback_distribution(canvas, guess, feedback_map, possible_solutions):
    if not guess:
        return

    feedback_patterns = collections.defaultdict(int)
    for solution in possible_solutions:
        feedback = feedback_map.get((guess, solution))
        if feedback:
            feedback_patterns[feedback] += 1

    if not feedback_patterns:
        return

    # Clear the previous plot
    for widget in canvas.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
    labels, counts = zip(*sorted(feedback_patterns.items()))

    ax.bar(labels, counts, color='skyblue')
    ax.set_xlabel("Feedback Pattern")
    ax.set_ylabel("Number of Solutions")
    ax.set_title(f"Feedback Distribution for '{guess.upper()}'")
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right")
    fig.tight_layout()

    chart = FigureCanvasTkAgg(fig, master=canvas)
    chart.draw()
    chart.get_tk_widget().pack()

def plot_guess_distribution(results, max_tries, search_depth, optimization_metric, subset_mode, average_tries, output_filename="guess_distribution.png", random_seed=None):
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
    title = f"Wordle Solver Guess Distribution\n"
    title += f"(Depth={search_depth}, Metric={optimization_metric}, Subset={subset_mode}"
    if random_seed is not None:
        title += f", Seed={random_seed}"
    title += f", Avg. Guesses={average_tries:.2f})"
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(output_filename)
    plt.close()
    print(f"Guess distribution plot saved to {output_filename}")