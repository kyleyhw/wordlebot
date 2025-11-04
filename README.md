# Wordle Bot

This project is a Wordle bot that can play Wordle and solve it.

## Directory Structure

```
/
├───README.md
├───environment.yml
├───feedback_map.json
├───funcs.py
├───generate_feedback_map.py
├───gui_game.py
├───gui_helper.py
├───main.py
├───play_game.py
├───rules.py
├───solver.py
├───visualizations.py
├───wordle_helper.py
├───word_lists.py
├───__pycache__/
│   ├───funcs.cpython-310.pyc
│   ├───funcs.cpython-39.pyc
│   ├───rules.cpython-310.pyc
│   ├───rules.cpython-39.pyc
│   ├───solver.cpython-310.pyc
│   └───solver.cpython-39.pyc
├───checkpoints/
├───data/
│   ├───frequency_data.txt
│   ├───wordle_allowed_guesses.txt
│   ├───wordle_allowed_guesses_unsorted.txt
│   └───wordle_answers.txt
├───docs/
│   ├───generate_feedback_map.md
│   ├───gui_game.md
│   ├───gui_helper.md
│   ├───main.md
│   ├───play_game.md
│   ├───rules.md
│   ├───solver.md
│   ├───word_lists.md
│   └───wordle_helper.md
└───test_reports/
```

## Documentation

- [`generate_feedback_map.md`](./docs/generate_feedback_map.md)
- [`gui_game.md`](./docs/gui_game.md)
- [`gui_helper.md`](./docs/gui_helper.md)
- [`main.md`](./docs/main.md)
- [`play_game.md`](./docs/play_game.md)
- [`rules.md`](./docs/rules.md)
- [`solver.md`](./docs/solver.md)
- [`word_lists.md`](./docs/word_lists.md)
- [`wordle_helper.md`](./docs/wordle_helper.md)

## Overview

Wordle is a web-based word game created and developed by Welsh software engineer Josh Wardle [[1]](#ref-wardle-2022). The game's objective is to guess a five-letter word in six attempts. After each guess, the player receives feedback in the form of colored tiles, indicating whether the letters they guessed are in the correct position, in the word but in the wrong position, or not in the word at all.

This project implements a Wordle solver that uses an information-theoretic approach to make optimal guesses. The solver's strategy is based on the concept of entropy, which is a measure of the uncertainty or randomness of a system. In the context of Wordle, the entropy of a guess is a measure of how much information that guess is expected to provide, on average. The solver chooses the guess with the highest entropy, which is the guess that is expected to narrow down the list of possible solutions the most [[2]](#ref-shannon-1948).

## Setup

To set up the environment, you will need to have conda installed. Then, you can create the environment from the `environment.yml` file:

```
conda env create -f environment.yml
```

Then, activate the environment:

```
conda activate wordlebot
```

## Usage

To play the game, run:

```
python play_game.py
```

To run the solver, run:

```
python main.py
```

To play the game with a GUI, run:

```
python gui_game.py
```

To use the interactive Wordle helper, run:

```
python wordle_helper.py
```

To use the GUI Wordle helper, run:

```
python gui_helper.py
```

To generate the feedback map cache (e.g., for the full word list), run:

```
python generate_feedback_map.py --full_list
```

## References

<a id="ref-wardle-2022"></a>
[1] Wardle, J. (2022). *Wordle*. Retrieved from https://www.nytimes.com/games/wordle/index.html

<a id="ref-shannon-1948"></a>
[2] Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, *27*(3), 379-423.