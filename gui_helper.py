import tkinter as tk
from tkinter import messagebox
import collections

from solver import solver
from word_lists import word_list_manager

NUM_RECOMMENDATIONS = 5 # Number of top recommendations to display

class WordleGUIHelper:
    def __init__(self, master, search_depth, optimization_metric):
        self.master = master
        master.title("Wordle Helper")

        self.solver = solver(search_depth=search_depth, optimization_metric=optimization_metric)
        self.guess_history = [] # List of (guess_word, feedback_str) tuples

        # --- GUI Elements ---
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        # Guess Input
        tk.Label(self.master, text="Your Guess:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.guess_entry = tk.Entry(self.master, width=10)
        self.guess_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        self.guess_entry.bind("<Return>", lambda event: self.process_guess())

        # Feedback Input (5 letter boxes)
        self.feedback_frames = []
        self.feedback_labels = []
        self.feedback_states = ['b'] * 5 # b: black, y: yellow, g: green

        tk.Label(self.master, text="Feedback:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        for i in range(5):
            frame = tk.Frame(self.master, bd=2, relief="groove")
            frame.grid(row=1, column=i+1, pady=5, padx=2)
            self.feedback_frames.append(frame)

            label = tk.Label(frame, text=" ", width=4, height=2, font=("Arial", 16, "bold"), bg="lightgray")
            label.pack()
            self.feedback_labels.append(label)

            # Bind click events
            label.bind("<Button-1>", lambda event, idx=i: self.set_feedback(idx, 'g')) # Left click for Green
            label.bind("<Button-3>", lambda event, idx=i: self.set_feedback(idx, 'y')) # Right click for Yellow
            label.bind("<Button-2>", lambda event, idx=i: self.set_feedback(idx, 'b')) # Middle click for Black (or scroll click)
            # For macOS, Button-2 (middle click) might be Button-3, and Button-3 (right click) might be Button-2
            # Let's ensure right click is yellow, and left click is green, and a third option for black.
            # On some systems, Button-2 is middle click, Button-3 is right click.
            # We'll use Button-1 for green, Button-3 for yellow, and Button-2 for black (if available, otherwise it cycles)

        # Submit Button
        self.submit_button = tk.Button(self.master, text="Submit Guess", command=self.process_guess)
        self.submit_button.grid(row=2, column=0, columnspan=6, pady=10)

        # History Display
        tk.Label(self.master, text="Guess History:").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.history_text = tk.Text(self.master, height=6, width=40, state="disabled", wrap="word")
        self.history_text.grid(row=4, column=0, columnspan=6, pady=5, padx=5)

        # Recommendations Display
        tk.Label(self.master, text="Recommendations:").grid(row=5, column=0, pady=5, padx=5, sticky="w")
        self.recommendations_text = tk.Text(self.master, height=10, width=40, state="disabled", wrap="word")
        self.recommendations_text.grid(row=6, column=0, columnspan=6, pady=5, padx=5)

        # Reset Button
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game)
        self.reset_button.grid(row=7, column=0, columnspan=6, pady=10)

    def set_feedback(self, index, color_code):
        self.feedback_states[index] = color_code
        self.update_feedback_display()

    def update_feedback_display(self):
        color_map = {
            'b': "lightgray", # Black
            'y': "gold",      # Yellow
            'g': "mediumseagreen" # Green
        }
        for i, state in enumerate(self.feedback_states):
            self.feedback_labels[i].config(bg=color_map[state])
            # Also update the letter in the feedback box if a guess was entered
            if self.guess_entry.get() and len(self.guess_entry.get()) == 5:
                self.feedback_labels[i].config(text=self.guess_entry.get()[i].upper())
            else:
                self.feedback_labels[i].config(text=" ")

    def process_guess(self):
        guess_word = self.guess_entry.get().lower()
        feedback_str = "".join(self.feedback_states)

        if len(guess_word) != 5 or not guess_word.isalpha():
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word.")
            return
        
        self.guess_history.append((guess_word, feedback_str))
        self.update_history_display()

        if feedback_str == "ggggg":
            messagebox.showinfo("Congratulations!", f"You solved it in {len(self.guess_history)} guesses!")
            self.display_recommendations([]) # Clear recommendations
            return

        # Get recommendations from solver
        # This part needs modification in solver.py to return multiple guesses and stats
        # For now, it will just get the single best guess
        next_guesses_with_stats = self.solver.get_next_guess(self.guess_history, num_recommendations=NUM_RECOMMENDATIONS)
        self.display_recommendations(next_guesses_with_stats)

        self.guess_entry.delete(0, tk.END)
        self.feedback_states = ['b'] * 5 # Reset feedback for next guess
        self.update_feedback_display()

    def update_history_display(self):
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        for i, (guess_word, feedback_colors) in enumerate(self.guess_history):
            display_line = []
            for j, char in enumerate(guess_word):
                color = feedback_colors[j]
                if color == 'g':
                    display_line.append(f"[{char.upper()}]") # Green
                elif color == 'y':
                    display_line.append(f"({char.upper()})") # Yellow
                else:
                    display_line.append(f" {char.upper()} ") # Black
            self.history_text.insert(tk.END, f"Guess {i+1}: {' '.join(display_line)}\n")
        self.history_text.config(state="disabled")

    def display_recommendations(self, recommendations):
        self.recommendations_text.config(state="normal")
        self.recommendations_text.delete(1.0, tk.END)
        if not recommendations:
            self.recommendations_text.insert(tk.END, "No recommendations available.")
        else:
            self.recommendations_text.insert(tk.END, "Top Recommendations:\n")
            # Assuming recommendations is a list of (guess, score) or (guess, stats_dict)
            for i, rec in enumerate(recommendations):
                if isinstance(rec, tuple):
                    guess, score = rec
                    self.recommendations_text.insert(tk.END, f"{i+1}. {guess.upper()} (Score: {score:.4f})\n")
                else:
                    # If solver returns just a string for now
                    self.recommendations_text.insert(tk.END, f"{i+1}. {rec.upper()}\n")
        self.recommendations_text.config(state="disabled")

    def reset_game(self):
        self.guess_history = []
        self.guess_entry.delete(0, tk.END)
        self.feedback_states = ['b'] * 5
        self.update_feedback_display()
        self.update_history_display()
        
        # Get initial recommendation
        initial_recommendation = self.solver.get_next_guess([], num_recommendations=NUM_RECOMMENDATIONS)
        self.display_recommendations(initial_recommendation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GUI Wordle Helper to suggest the best next guess.")
    parser.add_argument("--depth", type=int, default=1,
                        help="Search depth for the solver (e.g., 1 for greedy, 2 for looking ahead).")
    parser.add_argument("--metric", type=str, default="min_avg_remaining",
                        choices=["min_max_remaining", "min_avg_remaining", "min_avg_guesses"],
                        help="Optimization metric for the solver.")
    args = parser.parse_args()

    root = tk.Tk()
    app = WordleGUIHelper(root, search_depth=args.depth, optimization_metric=args.metric)
    root.mainloop()
