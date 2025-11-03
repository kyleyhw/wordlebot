import tkinter as tk
from tkinter import messagebox
import random
import argparse

from rules import game
from solver import solver
from visualizations import plot_feedback_distribution
import word_lists

class WordleGUI:
    def __init__(self, master):
        self.master = master
        master.title("Wordle")
        master.geometry("800x600")

        self.current_guess_num = 0
        self.guess_history = []
        self.solution = ""

        self.allowed_guesses = word_lists.get_allowed_guesses()
        self.possible_solutions = word_lists.get_possible_solutions()

        self.solver_instance = solver()

        self.create_widgets()
        self.start_new_game()

    def create_widgets(self):
        self.guess_frames = []
        self.letter_labels = []

        # Create 6 rows for guesses
        for r in range(6):
            frame = tk.Frame(self.master)
            frame.pack(pady=2)
            self.guess_frames.append(frame)

            row_labels = []
            # Create 5 letter boxes for each row
            for c in range(5):
                label = tk.Label(frame, text="", width=4, height=2, relief="solid", borderwidth=1, font=("Arial", 16, "bold"))
                label.pack(side=tk.LEFT, padx=2)
                row_labels.append(label)
            self.letter_labels.append(row_labels)

        # Input entry
        self.input_entry = tk.Entry(self.master, width=10, font=("Arial", 16))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<Return>", self.make_guess_event)

        # Guess button
        self.guess_button = tk.Button(self.master, text="Guess", command=self.make_guess)
        self.guess_button.pack(pady=5)

        # New Game button
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(pady=5)

        # Create a canvas for the plot
        self.plot_canvas = tk.Canvas(self.master, width=400, height=400, bg='grey')
        self.plot_canvas.pack(side=tk.RIGHT, padx=10)

    def start_new_game(self):
        self.solution = random.choice(self.possible_solutions)
        self.game_instance = game(solution=self.solution)
        self.current_guess_num = 0
        self.guess_history = []

        # Clear the board
        for r in range(6):
            for c in range(5):
                self.letter_labels[r][c].config(text="", bg="SystemButtonFace")

        # Clear the plot
        for widget in self.plot_canvas.winfo_children():
            widget.destroy()
        
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(state=tk.NORMAL)
        self.guess_button.config(state=tk.NORMAL)
        print(f"Solution (for debugging): {self.solution}") # Remove later

    def make_guess_event(self, event):
        self.make_guess()

    def make_guess(self):
        guess_word = self.input_entry.get().lower()
        self.input_entry.delete(0, tk.END)

        if len(guess_word) != 5 or not guess_word.isalpha():
            messagebox.showwarning("Invalid Guess", "Please enter a 5-letter word.")
            return
        if guess_word not in self.allowed_guesses:
            messagebox.showwarning("Invalid Guess", "Word not in list.")
            return

        feedback = self.game_instance.enter(guess=guess_word)
        self.guess_history.append((guess_word, feedback))

        self.update_board()

        # Update the plot
        plot_feedback_distribution(self.plot_canvas, guess_word, self.solver_instance.feedback_map, self.possible_solutions)

        if "".join(feedback) == "ggggg":
            messagebox.showinfo("Wordle", f"You won in {self.current_guess_num + 1} guesses!")
            self.end_game()
        elif self.current_guess_num == 5: # 6th guess (index 5)
            messagebox.showinfo("Wordle", f"You lost! The word was {self.solution.upper()}.")
            self.end_game()
        else:
            self.current_guess_num += 1

    def update_board(self):
        for i, (guess_word, feedback_colors) in enumerate(self.guess_history):
            for j, char in enumerate(guess_word):
                label = self.letter_labels[i][j]
                label.config(text=char.upper())
                color = feedback_colors[j]
                if color == 'g':
                    label.config(bg="#6aaa64") # Green
                elif color == 'y':
                    label.config(bg="#c9b458") # Yellow
                else:
                    label.config(bg="#787c7e") # Gray

    def end_game(self):
        self.input_entry.config(state=tk.DISABLED)
        self.guess_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Wordle GUI.")
    parser.add_argument("--subset", action="store_true", help="Use a subset of words for testing.")
    args = parser.parse_args()

    if args.subset:
        word_lists.SUBSET_MODE = True

    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()
