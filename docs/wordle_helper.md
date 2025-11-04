# Wordle Helper Documentation

## Overview

The `wordle_helper.py` script provides an interactive command-line interface (CLI) for assisting users in playing Wordle. It leverages the advanced Wordle solver implemented in `solver.py` to suggest optimal next guesses based on the current game state (previous guesses and their corresponding feedback). This tool is designed for users who want to improve their Wordle game by utilizing an information-theoretic approach to guess selection without running full simulations.

## Design Choices and Implementation Details

The `wordle_helper.py` script is structured to facilitate a turn-based interaction with the user.

### 1. Initialization

Upon execution, the script initializes an instance of the `solver` class. This involves:
- Loading allowed guesses and possible solutions from `word_lists.py`.
- Pre-calculating the feedback map for all guess-solution pairs, which is a computationally intensive but one-time operation. This map is cached to speed up subsequent runs [[1]](#ref-solver-doc).
- Calculating the best initial guess based on the configured `search_depth` and `optimization_metric`. This pre-calculation ensures that the first recommendation is readily available.

The `search_depth` and `optimization_metric` parameters for the solver can be configured via command-line arguments (`--depth` and `--metric`), allowing users to experiment with different solver strategies.

### 2. Interactive Game Loop

The core of the helper is an infinite loop that guides the user through the Wordle game:

#### a. Display Current Game State

The `display_guess_history` function presents a clear visual representation of all previous guesses and their feedback. This helps the user track their progress and ensures they can accurately input the next game state. The feedback is color-coded using square brackets for green letters, parentheses for yellow letters, and spaces for black letters, mirroring a common visual style for Wordle feedback.

#### b. First Guess Recommendation

If no guesses have been made yet, the script directly provides the pre-calculated best initial guess. This eliminates the need for the user to input anything for the first turn, streamlining the start of the game.

#### c. Subsequent Guess Input and Feedback

For subsequent turns, the user is prompted to:
- Enter their last guess. Basic validation ensures the input is a 5-letter word. A warning is issued if the word is not in the solver's allowed list, but the process continues to accommodate potential variations or user errors.
- Enter the feedback received from Wordle (e.g., 'bybyb'). The `get_feedback_from_user` function validates this input to ensure it consists of 5 characters, each being 'b' (black), 'y' (yellow), or 'g' (green).

#### d. Game End Condition

If the user's feedback is 'ggggg' (all green), the script congratulates the user and terminates, indicating a successful solve.

#### e. Next Guess Recommendation

After processing the user's input and updating the internal `guess_history`, the `solver.get_next_guess(guess_history)` method is called. This method filters the list of possible solutions based on the `guess_history` and then uses the solver's logic (based on `search_depth` and `optimization_metric`) to determine the most informative next guess. The recommended guess is then displayed to the user.

### 3. Continuation or Exit

After each recommendation, the user is given the option to continue for the next guess or quit the helper.

## Usage

To use the Wordle Helper, navigate to the project's root directory in your terminal and run:

```bash
python wordle_helper.py
```

You can also specify solver parameters:

```bash
python wordle_helper.py --depth 2 --metric min_avg_guesses
```

Follow the on-screen prompts to input your guesses and the feedback received from the Wordle game.

## References

<a id="ref-solver-doc"></a>
[1] See `solver.md` for detailed documentation on the Wordle solver's implementation, including feedback map pre-calculation and optimization metrics.
