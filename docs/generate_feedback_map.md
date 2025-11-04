# Generate Feedback Map Documentation

## Overview

The `generate_feedback_map.py` script is a utility designed to pre-calculate and cache the Wordle solver's feedback map. This map stores the feedback (e.g., "bybyb") for every possible guess-solution pair. Generating this map is a computationally intensive process, especially when using large word lists. By separating this generation into a dedicated script, users can:

1.  Generate the feedback map once for a specific word list configuration (e.g., the full list or a specific subset).
2.  Then, run simulations or interactive helpers with different word list configurations. The solver will load the appropriate cached map, avoiding redundant calculations.

This approach significantly speeds up subsequent runs of the solver, as the most time-consuming pre-calculation is done only when necessary.

## Design Choices and Implementation Details

The script directly generates the feedback map by iterating through all possible guess-solution pairs and calculating the feedback for each. It then serializes this map using `pickle` and saves it to a file.

### 1. Word List Configuration

The script utilizes the `word_list_manager` (from `word_lists.py`) to obtain the allowed guesses and possible solutions. The configuration of these word lists (e.g., using the full list or a subset) is determined by how `word_list_manager` is initialized or configured prior to calling `generate_and_save_feedback_map`.

### 2. Feedback Map Generation

The `generate_and_save_feedback_map` function performs the following steps:

-   Retrieves the `allowed_guesses` and `possible_solutions` from `word_list_manager`.
-   Iterates through every combination of `guess` from `allowed_guesses` and `solution` from `possible_solutions`.
-   For each pair, it calls `get_feedback(guess, solution)` to determine the Wordle feedback pattern.
-   Stores the `(guess, solution)` -> `feedback` mapping in a dictionary.
-   Finally, it serializes this dictionary using `pickle` and saves it to the specified output file.

### 3. `get_feedback` Function

The `get_feedback` function, adapted from `rules.py`, determines the Wordle feedback for a given `guess` and `solution`. It performs two passes:

-   **First pass**: Identifies 'green' letters (correct letter in the correct position).
-   **Second pass**: Identifies 'yellow' letters (correct letter in the wrong position) and 'black' letters (letter not in the solution).

## Usage

To generate the feedback map cache, run the script with an optional `--output_file` argument:

```bash
python generate_feedback_map.py --output_file my_feedback_map.pkl
```

If `--output_file` is not provided, the default filename `feedback_map.pkl` will be used.

**Important:** The word lists used for generating the feedback map are determined by the current configuration of `word_list_manager`. Ensure `word_list_manager` is configured as desired (e.g., full list or a specific subset) *before* running this script.

After generating the feedback map, other scripts (like `main.py` or `solver.py`) will automatically load this pre-calculated map if it exists in the expected location.

## References

<a id="ref-solver-doc"></a>
[1] See `solver.md` for detailed documentation on the Wordle solver's implementation, including how it utilizes the pre-calculated feedback map.