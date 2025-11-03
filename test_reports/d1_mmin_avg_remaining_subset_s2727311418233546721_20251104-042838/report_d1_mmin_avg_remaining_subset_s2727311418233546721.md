# Test Report: Wordle Solver Simulation

## 1. What was done
A simulation was run using the Wordle solver against a subset of 100 words from the `wordle_answers.txt` list (Random Seed: 2727311418233546721). The set of allowed guesses was also limited to this same subset.

## 2. Why it was done
This test was performed to evaluate the performance of the Wordle solver.

## 3. What was specifically tested
The solver's performance was tested with the following configuration:
*   **Search Depth**: 1 (greedy approach)
*   **Optimization Metric**: `min_avg_remaining` (minimizing average remaining solutions)
*   **Dataset**: Subset of 100 words from `wordle_answers.txt` for both solutions and allowed guesses (Random Seed: 2727311418233546721).

## 4. Results
```

--- Solver Performance Report ---
Total solutions simulated: 100
Used a subset of 100 words for both solutions and guesses (Random Seed: 2727311418233546721).
Average guesses per game: 6.72

Guess Distribution:
  1 tries: 1 solutions
  2 tries: 2 solutions
  3 tries: 1 solutions
  4 tries: 2 solutions
  6 tries: 2 solutions
  Failed (>6 tries): 92 solutions

Solutions that failed to be solved within 6 tries:
- brass
- cyber
- pride
- would
- grove
- golem
- three
- fritz
- cheer
- quoth
- lofty
- offer
- cease
- floor
- carat
- fairy
- steal
- trite
- ditty
- comfy
- elder
- bible
- tweed
- rowdy
- swine
- horde
- frame
- unify
- fugue
- pubic
- pulpy
- canon
- chest
- flair
- gruel
- plunk
- ocean
- lobby
- truer
- sloth
- boney
- paper
- steam
- sadly
- ditch
- eager
- gauge
- frost
- idiom
- admin
- buddy
- lowly
- flood
- nymph
- owner
- helix
- navel
- leafy
- rerun
- perch
- safer
- miser
- tunic
- plain
- blink
- write
- spook
- bribe
- cough
- audio
- cobra
- rajah
- tenth
- straw
- merge
- chirp
- snout
- trawl
- depth
- spill
- wooer
- solar
- above
- swear
- vapor
- broom
- alike
- marry
- query
- posse
- vital
- abbey

Runtime: 131.51 seconds
```

## 5. Guess Distribution Plot

![Guess Distribution](guess_distribution_d1_mmin_avg_remaining_subset_s2727311418233546721.png)

## 6. Runtime
The simulation completed in 131.51 seconds.
