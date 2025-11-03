# Word Lists (`word_lists.py`)

## 1. Purpose

The `word_lists.py` module centralizes the loading and management of the word lists used by the Wordle solver and game interfaces. It provides a single source of truth for the allowed guesses and possible solutions, and it implements a "subset mode" for testing and debugging.

## 2. Subset Mode

To facilitate rapid testing and debugging, this module includes a `SUBSET_MODE`. When this mode is enabled, the functions in this module will return a small subset of the full word lists. This is particularly useful for testing the solver's logic without having to run a full simulation, which can be very time-consuming.

*   **`SUBSET_MODE` (bool)**: A global flag that controls whether to use the full word lists or the subset. This flag is intended to be set at runtime by the script that imports this module (e.g., via a command-line argument).
*   **`SUBSET_SIZE` (int)**: A constant that defines the size of the subset to be used when `SUBSET_MODE` is enabled.

## 3. Functions

### `_load_word_lists()`

*   **Purpose**: A private function that loads the word lists from the data files (`wordle_allowed_guesses.txt` and `wordle_answers.txt`).
*   **Implementation Details**: This function is called automatically by `get_allowed_guesses()` or `get_possible_solutions()` the first time they are invoked. The loaded lists are stored in private global variables (`_allowed_guesses` and `_possible_solutions`) to avoid repeated file I/O.

### `get_allowed_guesses()`

*   **Purpose**: Returns the list of allowed guesses.
*   **Returns**: (list of str) If `SUBSET_MODE` is `True`, it returns a subset of the possible solutions. Otherwise, it returns the full list of allowed guesses.

### `get_possible_solutions()`

*   **Purpose**: Returns the list of possible solutions.
*   **Returns**: (list of str) If `SUBSET_MODE` is `True`, it returns a subset of the possible solutions. Otherwise, it returns the full list of possible solutions.

## 4. Dependencies

*   `random`: Although not directly used in this module, it is used by the scripts that consume the word lists for selecting random solutions.
*   `data/wordle_allowed_guesses.txt`: The text file containing the list of all allowed guesses.
*   `data/wordle_answers.txt`: The text file containing the list of all possible solutions.
