# GUI Wordle Helper Documentation

## Overview

The `gui_helper.py` script provides a graphical user interface (GUI) for the Wordle helper. It allows users to interactively input their guesses and the feedback received from the Wordle game, and in return, receive a list of recommended next guesses along with their associated statistics. This GUI aims to provide a more intuitive and user-friendly experience compared to the command-line interface.

## Design Choices and Implementation Details

The GUI is built using Python's built-in `tkinter` library, ensuring broad compatibility without external dependencies.

### 1. User Interface Layout

The GUI is organized into several key sections:

-   **Guess Input**: A text entry field where the user types their 5-letter Wordle guess.
-   **Feedback Input**: Five individual letter boxes are provided to input the feedback for each letter of the guess. This is the most interactive part:
    -   **Left-click**: Sets the letter's feedback to **Green** (correct letter, correct position).
    -   **Right-click**: Sets the letter's feedback to **Yellow** (correct letter, wrong position).
    -   **Middle-click (or scroll-click)**: Sets the letter's feedback to **Black** (letter not in the word). If a middle-click is not available, the feedback can be cycled through green, yellow, and black by repeated left-clicks.
    The background color of each letter box visually indicates the feedback state.
-   **Submit Guess Button**: Triggers the processing of the current guess and feedback, updating the game state and requesting new recommendations from the solver.
-   **Guess History Display**: A read-only text area that shows all previous guesses and their feedback, providing a clear record of the game's progression.
-   **Recommendations Display**: A read-only text area that lists the top recommended guesses from the solver, along with their calculated scores (e.g., expected remaining solutions, average guesses).
-   **Reset Game Button**: Clears the current game state and starts a new Wordle puzzle.

### 2. Integration with the Wordle Solver

The `gui_helper.py` script instantiates the `solver` class from `solver.py`. It leverages the `get_next_guess` method of the solver, which has been enhanced to return a list of top `N` recommended guesses, each paired with its calculated score. This allows the GUI to present multiple options to the user, along with quantitative data to aid their decision.

### 3. Feedback Mechanism

The click-based feedback system is implemented by binding mouse events to each letter's display label. This provides a quick and visual way for users to input the feedback they receive from the actual Wordle game. The `feedback_states` list internally tracks the 'b', 'y', 'g' status for each letter.

### 4. Game Flow

-   **Initialization**: Upon launching, the GUI initializes the solver and immediately displays the top recommendations for the first guess.
-   **User Input**: The user types their guess and sets the feedback for each letter by clicking the respective boxes.
-   **Processing**: Clicking "Submit Guess" validates the input, updates the `guess_history`, and calls the solver to get new recommendations.
-   **Display Updates**: The guess history and recommendations areas are updated to reflect the new game state.
-   **Game End**: If the feedback is all green, a congratulatory message is displayed, and recommendations are cleared.

## Usage

To use the GUI Wordle Helper, navigate to the project's root directory in your terminal and run:

```bash
python gui_helper.py
```

The GUI window will appear, and you can start interacting with it immediately.

## References

<a id="ref-solver-doc"></a>
[1] See `solver.md` for detailed documentation on the Wordle solver's implementation, including feedback map pre-calculation and optimization metrics.
