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
