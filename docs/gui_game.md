# GUI Game (`gui_game.py`)

## 1. Purpose

The `gui_game.py` module provides a Graphical User Interface (GUI) for playing the Wordle game [[1]](#ref-wardle-2022). It offers a more visual and interactive experience compared to the CLI, allowing users to play Wordle with a familiar graphical layout.

## 2. Features

*   **Graphical Board**: Displays the Wordle grid with letter boxes that change color according to feedback.
*   **Interactive Input**: Users type guesses into an entry field and submit them via a button or by pressing Enter.
*   **Visual Feedback**: Letters in the grid are colored (green, yellow, gray) to match Wordle's feedback system.
*   **Input Validation**: Ensures guesses are 5-letter alphabetic words present in the allowed word list.
*   **6-Attempt Limit**: Enforces the standard Wordle rule of a maximum of 6 guesses.
*   **Win/Loss Pop-ups**: Uses message boxes to clearly inform the player of game outcomes.
*   **New Game Functionality**: A dedicated button to start a fresh game with a new random solution.
*   **Solution Selection**: A new random solution is chosen from `wordle_answers.txt` for each game.
*   **Feedback Distribution Plot**: After each guess, a histogram is displayed showing the distribution of feedback patterns for that guess against all possible solutions. This visualization helps the player understand the quality of their guess.

## 3. How to Play

To play the Wordle game via the GUI, navigate to the project's root directory in your terminal and run the following command:

```bash
python3 gui_game.py
```

A new window will open, presenting the Wordle game board. Type your 5-letter guess into the input field at the bottom and click the "Guess" button or press Enter. The board will update with color-coded feedback, and a plot will be generated to show the feedback distribution.

## 4. Class: `WordleGUI`

### `__init__(self, master)`

*   **Purpose**: Initializes the GUI application, sets up the main window, loads word lists, and creates the game widgets.
*   **Parameters**:
    *   `master` (tk.Tk): The root Tkinter window.
*   **Implementation Details**:
    *   Configures the main window's title, size, and resizability.
    *   Loads `wordle_allowed_guesses.txt` and `wordle_answers.txt` into `self.allowed_guesses` and `self.possible_solutions` respectively.
    *   Initializes the `solver` to get access to the `feedback_map`.
    *   Calls `create_widgets()` to build the GUI elements.
    *   Calls `start_new_game()` to set up the first game.

### `create_widgets(self)`

*   **Purpose**: Constructs all the visual components of the Wordle game interface.
*   **Implementation Details**: 
    *   Creates 6 `tk.Frame` widgets, each representing a row for a guess.
    *   Within each frame, creates 5 `tk.Label` widgets to display individual letters, styled with borders and bold font. These labels are stored in `self.letter_labels` for easy access and updating.
    *   Creates a `tk.Entry` widget for user input, bound to the `make_guess_event` method for Enter key presses.
    *   Creates "Guess" and "New Game" `tk.Button` widgets, linked to their respective methods.
    *   Creates a `tk.Canvas` to display the feedback distribution plot.

### `start_new_game(self)`

*   **Purpose**: Resets the game state and prepares the GUI for a new round of Wordle.
*   **Implementation Details**: 
    *   Selects a new random `solution` word.
    *   Initializes a fresh `game` instance from `rules.py`.
    *   Clears the `guess_history` and resets `current_guess_num`.
    *   Resets all `letter_labels` on the board to empty text and default background color.
    *   Clears the feedback distribution plot.
    *   Re-enables the input entry and guess button.

### `make_guess_event(self, event)`

*   **Purpose**: Event handler for the Enter key press in the input field.
*   **Implementation Details**: Simply calls `self.make_guess()`.

### `make_guess(self)`

*   **Purpose**: Processes the user's guess, validates it, gets feedback, updates the board, and checks for game-ending conditions.
*   **Implementation Details**: 
    *   Retrieves the guess from `self.input_entry` and clears the entry field.
    *   Performs validation checks (length, alphabetic, presence in `allowed_guesses`). Shows `messagebox.showwarning` for invalid inputs.
    *   Calls `self.game_instance.enter()` to obtain feedback.
    *   Appends the guess and feedback to `self.guess_history`.
    *   Calls `self.update_board()` to refresh the GUI.
    *   Calls `plot_feedback_distribution()` to update the feedback distribution plot.
    *   Checks if the guess was correct (`"ggggg"`) or if the maximum number of tries has been reached. Displays `messagebox.showinfo` for win/loss and calls `self.end_game()`.
    *   Increments `self.current_guess_num`.

### `update_board(self)`

*   **Purpose**: Updates the visual representation of the Wordle board based on the `guess_history`.
*   **Implementation Details**: 
    *   Iterates through the `guess_history`.
    *   For each guess, it updates the `text` of the corresponding `tk.Label` widgets with the guessed letters.
    *   Sets the `bg` (background) color of the labels based on the feedback:
        *   `#6aaa64` for green.
        *   `#c9b458` for yellow.
        *   `#787c7e` for gray (black feedback).

### `end_game(self)`

*   **Purpose**: Disables user input and the guess button when the game concludes.
*   **Implementation Details**: 
    *   Sets the `state` of `self.input_entry` to `tk.DISABLED`.
    *   Sets the `state` of `self.guess_button` to `tk.DISABLED`.

## 5. Dependencies

*   `tkinter`: The standard Python GUI toolkit.
*   `tkinter.messagebox`: Used for displaying pop-up messages (warnings, win/loss notifications).
*   `random`: Used for selecting a random solution word.
*   `rules.py`: Provides the core `game` class and its `enter` method for processing guesses and generating feedback.
*   `solver.py`: Provides the `solver` class to get access to the `feedback_map`.
*   `visualizations.py`: Provides the `plot_feedback_distribution` function.
*   `wordle_allowed_guesses.txt`: A text file containing a list of all valid 5-letter words that can be entered as guesses.
*   `wordle_answers.txt`: A text file containing a list of all possible 5-letter words that can be chosen as the secret solution.

## References

<a id="ref-wardle-2022"></a>
[1] Wardle, J. (2022). *Wordle*. Retrieved from https://www.nytimes.com/games/wordle/index.html
