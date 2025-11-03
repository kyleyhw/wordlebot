# Simulation and Analysis (`main.py`)

## 1. Purpose

The `main.py` module serves as the primary script for simulating the Wordle solver's performance. It orchestrates the interaction between the `solver` and `game` modules to evaluate how effectively the information theory solver can solve a large set of Wordle puzzles. This module is crucial for benchmarking the solver and understanding its strengths and limitations.

## 2. Design Rationale

### Checkpoint System

*   **Problem**: The simulation process can be very time-consuming, especially when running against the full list of possible Wordle solutions. If the simulation is interrupted for any reason (e.g., power outage, system crash, or user interruption), all progress would be lost.
*   **Solution**: A checkpoint system was implemented to save the simulation's state periodically. The state, which includes the results so far, the list of failed solutions, and the index of the last processed solution, is saved to a JSON file.
*   **Implementation**: Before starting the simulation, the script checks for the existence of a checkpoint file. If found, it loads the state from the file and resumes the simulation from where it left off. The state is saved after every `CHECKPOINT_INTERVAL` solutions are processed. This design choice makes the simulation more robust and resilient to interruptions.

## 3. How to Run Simulations

To run the simulations and generate the performance report, navigate to the project's root directory in your terminal and execute the following command:

```bash
python3 main.py
```

Be aware that the solver performs extensive pre-calculations (generating a feedback map for all guess-solution pairs and determining the best initial guess) and then runs simulations for over 2,000 possible solutions. This process can be computationally intensive and may take a significant amount of time to complete, depending on your system's specifications. Progress updates will be printed to the console during the simulation, thanks to the `tqdm` library [[1]](#ref-tqdm).

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

## References

<a id="ref-tqdm"></a>
[1] tqdm. (2019). A Fast, Extensible Progress Bar for Python and CLI. Retrieved from https://github.com/tqdm/tqdm
