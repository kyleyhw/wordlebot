# Simulation and Analysis (`main.py`)

## 1. Purpose

The `main.py` module serves as the primary script for simulating the Wordle solver's performance. It orchestrates the interaction between the `solver` and `game` modules to evaluate how effectively the information theory solver can solve a large set of Wordle puzzles. This module is crucial for benchmarking the solver and understanding its strengths and limitations.

## 2. Features

*   **Comprehensive Simulation**: Runs the solver against every possible Wordle solution word defined in `wordle_answers.txt`.
*   **Performance Metrics**: Collects data on the number of guesses required for each solution.
*   **Detailed Reporting**: Generates a summary report including:
    *   Total number of solutions simulated.
    *   Average number of guesses across all simulations.
    *   Distribution of guesses (how many solutions were solved in 1, 2, 3, 4, 5, or 6 tries).
    *   Identification of any solutions that the solver failed to find within the 6-attempt limit.

## 3. How to Run Simulations

To run the simulations and generate the performance report, navigate to the project's root directory in your terminal and execute the following command:

```bash
python3 main.py
```

Be aware that the solver performs extensive pre-calculations (generating a feedback map for all guess-solution pairs and determining the best initial guess) and then runs simulations for over 2,000 possible solutions. This process can be computationally intensive and may take a significant amount of time to complete, depending on your system's specifications. Progress updates will be printed to the console during the simulation.

## 4. Functions

### `run_simulation()`

*   **Purpose**: Orchestrates the entire simulation process, from solver initialization to report generation.
*   **Implementation Details**:
    *   Loads `wordle_allowed_guesses.txt` and `wordle_answers.txt`.
    *   Initializes an instance of the `solver.solver` class, which triggers its pre-calculation steps.
    *   Iterates through each `solution` in `possible_solutions_list`:
        *   Creates a new `rules.game` instance for each solution.
        *   Manages `guess_history` and `tries` for the current game.
        *   Repeatedly calls `wordle_solver.get_next_guess()` to get the optimal guess.
        *   Feeds the guess to `game_instance.enter()` to get feedback.
        *   Updates the `guess_history` for the solver.
        *   Records the number of tries if the solution is found, or marks it as a failure if `MAX_TRIES` is exceeded.
    *   After all simulations, it calculates and prints the performance report, including average guesses, guess distribution, and a list of failed solutions.

## 5. Dependencies

*   `random`: Used indirectly by `rules.game` for solution selection in individual game instances (though `main.py` iterates through all solutions).
*   `collections`: Specifically `collections.defaultdict` for aggregating guess distribution statistics.
*   `rules.py`: Provides the `game` class for simulating individual Wordle games.
*   `solver.py`: Provides the `solver` class, which determines the optimal guesses based on information theory.
*   `wordle_allowed_guesses.txt`: Contains the list of words that the solver can use as guesses.
*   `wordle_answers.txt`: Contains the comprehensive list of all possible Wordle solutions, against which the solver is tested.
