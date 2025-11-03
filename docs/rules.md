# Game Rules (`rules.py`)

## 1. Purpose

The `rules.py` module defines the core logic of the Wordle game. It encapsulates the rules for determining the feedback (green, yellow, or black) for a given guess against a secret solution word. This module is designed to be independent of any user interface or solver logic, allowing it to be used consistently across different parts of the project (CLI, GUI, or solver simulations).

## 2. Wordle Game Rules and Feedback Logic

The Wordle game involves guessing a 5-letter secret word within 6 attempts. After each guess, the player receives feedback on how close their guess was to the solution. This feedback is provided for each letter in the guess, using a color-coded system:

*   **Green (G)**: The letter is in the secret word and in the correct position.
*   **Yellow (Y)**: The letter is in the secret word but in the wrong position.
*   **Black (B)**: The letter is not in the secret word at all.

### Behavior of Repeated Letters (Edge Cases)

The handling of repeated letters in both the guess and the solution is a crucial aspect of Wordle's feedback logic. The rules ensure that each letter in the solution is "consumed" only once by a matching letter in the guess.

**Example Scenarios:**

1.  **Solution: `APPLE`**
    *   **Guess: `PAPER`**
        *   `P`: The first 'P' in "PAPER" matches the first 'P' in "APPLE" (Green).
        *   `A`: 'A' in "PAPER" matches 'A' in "APPLE" (Green).
        *   `P`: The second 'P' in "PAPER" is in the solution but in the wrong position. Since the first 'P' in "APPLE" was already consumed, this 'P' matches the second 'P' in "APPLE" (Yellow).
        *   `E`: 'E' in "PAPER" matches 'E' in "APPLE" (Green).
        *   `R`: 'R' is not in "APPLE" (Black).
        *   **Feedback: `G G Y G B`**

2.  **Solution: `FLOOR`**
    *   **Guess: `ROBOT`**
        *   `R`: 'R' is in "FLOOR" but in the wrong position (Yellow).
        *   `O`: The first 'O' in "ROBOT" is in the solution but in the wrong position. It matches the first 'O' in "FLOOR" (Yellow).
        *   `B`: 'B' is not in "FLOOR" (Black).
        *   `O`: The second 'O' in "ROBOT" is in the solution but in the wrong position. Since the first 'O' in "FLOOR" was already consumed, this 'O' matches the second 'O' in "FLOOR" (Yellow).
        *   `T`: 'T' is not in "FLOOR" (Black).
        *   **Feedback: `Y Y B Y B`**

3.  **Solution: `SWEET`**
    *   **Guess: `TEASE`**
        *   `T`: 'T' is in "SWEET" but in the wrong position (Yellow).
        *   `E`: The first 'E' in "TEASE" is in the solution and in the correct position (Green).
        *   `A`: 'A' is not in "SWEET" (Black).
        *   `S`: 'S' is in "SWEET" but in the wrong position (Yellow).
        *   `E`: The second 'E' in "TEASE" is in the solution but in the wrong position. Since the first 'E' in "SWEET" was already consumed by the green 'E', this 'E' matches the second 'E' in "SWEET" (Yellow).
        *   **Feedback: `Y G B Y Y`**

## 3. Class: `game`

### `__init__(self, solution)`

*   **Purpose**: Initializes a new Wordle game instance with a specified solution word.
*   **Parameters**:
    *   `solution` (str): The 5-letter word that the player (or solver) needs to guess.
*   **Implementation Details**:
    *   Stores the `solution` internally after splitting it into a list of characters for easier comparison.

### `enter(self, guess)`

*   **Purpose**: Processes a player's (or solver's) guess and returns the Wordle-standard feedback (colors).
*   **Parameters**:
    *   `guess` (str): The 5-letter word entered by the player.
*   **Returns**: (list of str) A list of 5 characters, where each character represents the feedback for the corresponding letter in the guess:
    *   `'g'` for "green" (correct letter, correct position)
    *   `'y'` for "yellow" (correct letter, wrong position)
    *   `'b'` for "black" (letter not in the solution)

### Detailed Feedback Algorithm (Two-Pass Approach)

The algorithm implements a crucial "two-pass" approach to correctly handle duplicate letters in both the guess and the solution, mimicking the official Wordle rules. This approach is essential to prevent erroneous "yellow" assignments for letters that should be "green," or overcounting letters that only appear a limited number of times in the solution.

**Pass 1: Identifying Green Letters**
1.  An initial `colors` array is created, filled with 'b' (black), assuming no matches.
2.  A mutable copy of the `solution` is made (`solution_split`). This copy allows letters to be "consumed" or marked as used, preventing them from being matched again in subsequent steps.
3.  The algorithm iterates through the `guess` and compares each letter with the letter at the *same position* in the `solution_split`.
4.  If a letter `guess[i]` matches `solution_split[i]`, it signifies a "green" match:
    *   `colors[i]` is set to `'g'`.
    *   `solution_split[i]` is marked as `None`. This crucial step ensures that this particular instance of the letter in the solution is no longer available to be matched as a "yellow" letter later. This prevents scenarios where, for example, guessing "APPLE" against "APPLY" would incorrectly mark the second 'P' as yellow if the first 'P' was already green.

**Pass 2: Identifying Yellow and Black Letters**
1.  The algorithm then iterates through the `guess` *again*.
2.  For each letter `guess[i]`, it first checks if `colors[i]` is *not* already 'g'. Letters already marked 'g' are ignored, as their status is definitively determined.
3.  If `colors[i]` is not 'g', the algorithm checks if `guess[i]` is present *anywhere* in the *remaining* (unmarked) `solution_split`.
4.  If `guess[i]` is found in `solution_split`, it signifies a "yellow" match:
    *   `colors[i]` is set to `'y'`.
    *   The *first occurrence* of `guess[i]` in `solution_split` is marked as `None`. Similar to the green pass, this "consumes" one instance of the letter from the solution, preventing it from being counted again if the guess contains duplicate letters (e.g., guessing "PAPER" against "APPLE" – only one 'P' in "PAPER" should match a yellow 'P' from "APPLE").
5.  If `guess[i]` is not found in the `solution_split` (either it was never there, or all instances of it have already been consumed by green or yellow matches), then `colors[i]` remains `'b'` (black).

This two-pass mechanism guarantees that each letter in the guess is evaluated against the available letters in the solution according to Wordle's precise rules.

## 4. Dependencies

*   `funcs.py`: Utilizes the `split` function to convert strings into character arrays. (Note: The `count_occurrences` function is no longer directly used in the refined `enter` method, but `split` is still essential.)