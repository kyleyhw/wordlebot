# Wordle Bot

This project implements a Wordle game and an optimal Wordle solver using an information theory approach. The goal of the solver is to minimize the number of guesses required to solve a Wordle puzzle, adhering to the 6-attempt limit. The project also includes both a Command Line Interface (CLI) and a Graphical User Interface (GUI) for playing the game.

## Project Structure

```
/Users/kylewong/PycharmProjects/wordlebot/
├───funcs.py
├───main.py
├───play_game.py
├───rules.py
├───solver.py
├───gui_game.py
├───README.md
├───.git/...
├───.idea/...
└───data/
    ├───frequency_data.txt
    ├───wordle_allowed_guesses_unsorted.txt
    ├───wordle_allowed_guesses.txt
    └───wordle_answers.txt
└───docs/
    ├───rules.md
    ├───solver.md
    ├───play_game.md
    ├───gui_game.md
    └───main.md
```

## Documentation Index

*   [Game Rules (`rules.py`)](docs/rules.md)
*   [Information Theory Solver (`solver.py`)](docs/solver.md)
*   [CLI Game (`play_game.py`)](docs/play_game.md)
*   [GUI Game (`gui_game.py`)](docs/gui_game.md)
*   [Simulation and Analysis (`main.py`)](docs/main.md)
