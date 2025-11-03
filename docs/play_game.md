# CLI Game (`play_game.py`)

## 1. Purpose

The `play_game.py` module provides a Command Line Interface (CLI) for playing the Wordle game [[1]](#ref-wardle-2022) interactively. It allows users to guess words, receive feedback, and experience the game directly from their terminal. This module serves as a user-friendly interface for human players and also as a testing ground for the core game logic defined in `rules.py`.

## 2. Features

*   **Interactive Gameplay**: Users can enter 5-letter guesses directly into the terminal.
*   **Clear Feedback**: Displays each guess with color-coded feedback (green, yellow, black) to indicate the correctness of letters and their positions.
*   **Guess History**: Maintains and displays a history of all previous guesses and their corresponding feedback, allowing players to track their progress.
*   **Input Validation**: Ensures that user-entered guesses are:
    *   Exactly 5 letters long.
    *   Composed only of alphabetic characters.
    *   Valid words found in the `wordle_allowed_guesses.txt` list.
*   **6-Attempt Limit**: Enforces the standard Wordle rule of a maximum of 6 guesses per game.
*   **Win/Loss Conditions**: Clearly notifies the player upon winning (guessing the word correctly) or losing (running out of attempts).
*   **Random Solution Selection**: A new random solution is chosen from `wordle_answers.txt` for each game.

## 3. How to Play

To play the Wordle game via the CLI, navigate to the project's root directory in your terminal and run the following command:

```bash
python3 play_game.py
```

To play the game with a subset of words for faster testing, use the `--subset` flag:

```bash
python3 play_game.py --subset
```

The game will then prompt you to enter your 5-letter guesses. Follow the on-screen instructions and feedback to deduce the secret word.

## 4. Functions

### `display_board(guess_history, tries_left)`

*   **Purpose**: Renders the current state of the Wordle board in the terminal.
*   **Parameters**:
    *   `guess_history` (list of tuples): A list where each tuple contains `(guess_word, feedback_colors)`.
    *   `tries_left` (int): The number of remaining guesses.
*   **Implementation Details**:
    *   Prints a formatted header with the number of tries left.
    *   Iterates through `guess_history` to display each past guess. Letters are presented with visual cues (e.g., `[G]` for green, `(Y)` for yellow, ` B ` for black) to represent the feedback.
    *   Prints empty lines for remaining guesses to visually represent the 6-row board.

### `play_wordle()`

*   **Purpose**: Contains the main game loop and orchestrates the interactive gameplay.
*   **Implementation Details**:
    *   Uses the `word_lists` module to get the word lists.
    *   Selects a random `solution` from the list of possible solutions.
    *   Initializes a `game` instance from `rules.py`.
    *   Manages `guess_history` and `tries` count.
    *   Enters a loop that continues until the word is guessed or `MAX_TRIES` (6) are exhausted.
    *   Inside the loop:
        *   Calls `display_board`.
        *   Prompts the user for input.
        *   Performs input validation.
        *   Calls `game_instance.enter()` to get feedback.
        *   Updates `guess_history`.
        *   Checks for win/loss conditions and displays appropriate messages.

## 5. Dependencies

*   `argparse`: For parsing command-line arguments.
*   `random`: Used for selecting a random solution word.
*   `sys`: Potentially used for system-level operations (though not explicitly used in the current version, it's a common utility for CLI apps).
*   `rules.py`: Provides the core `game` class and its `enter` method for processing guesses and generating feedback.
*   `word_lists.py`: Provides the word lists for the game.

## References

<a id="ref-wardle-2022"></a>
[1] Wardle, J. (2022). *Wordle*. Retrieved from https://www.nytimes.com/games/wordle/index.html
