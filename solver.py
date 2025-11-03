import collections
import math
import random
import sys
import json
import os
from tqdm import tqdm

from funcs import split

# --- Helper function to get feedback (copied and adapted from rules.py) ---
def get_feedback(guess, solution):
    colors = split('bbbbb')
    guess_split = split(guess)
    solution_split = list(split(solution)) # Use a mutable copy

    # First pass: Check for green letters
    for i, letter in enumerate(guess_split):
        if letter == solution_split[i]:
            colors[i] = 'g'
            solution_split[i] = None  # Mark as used

    # Second pass: Check for yellow and black letters
    for i, letter in enumerate(guess_split):
        if colors[i] != 'g':  # Only check if not already marked green
            if letter in solution_split:
                colors[i] = 'y'
                solution_split[solution_split.index(letter)] = None  # Mark as used
            else:
                colors[i] = 'b'
    return "".join(colors)

# --- Solver Class ---
class solver:
    def __init__(self, allowed_guesses_list, possible_solutions_list, search_depth=1, optimization_metric='min_avg_remaining'):
        self.allowed_guesses = allowed_guesses_list
        self.possible_solutions = possible_solutions_list
        self.search_depth = search_depth
        self.optimization_metric = optimization_metric
        self.feedback_map = {}
        self.best_initial_guesses_by_config = {}
        self._expected_guesses_memo = {}

        if self.optimization_metric not in ['min_max_remaining', 'min_avg_remaining', 'min_avg_guesses']:
            raise ValueError("optimization_metric must be 'min_max_remaining', 'min_avg_remaining', or 'min_avg_guesses'")

        feedback_map_cache_file = "feedback_map.json"
        if os.path.exists(feedback_map_cache_file):
            print("Solver: Loading feedback map from cache...")
            with open(feedback_map_cache_file, 'r') as f:
                feedback_map_str_keys = json.load(f)
            self.feedback_map = {tuple(eval(k)): v for k, v in feedback_map_str_keys.items()}
            print("Solver: Feedback map loaded from cache.")
        else:
            print("Solver: Pre-calculating feedback map...")
            # Pre-calculate feedback for all guess-solution pairs
            for guess in tqdm(self.allowed_guesses, desc="Pre-calculating feedback map"):
                for solution in self.possible_solutions:
                    self.feedback_map[(guess, solution)] = get_feedback(guess, solution)
            print("Solver: Feedback map pre-calculation complete.")
            print("Solver: Saving feedback map to cache...")
            feedback_map_str_keys = {str(k): v for k, v in self.feedback_map.items()}
            with open(feedback_map_cache_file, 'w') as f:
                json.dump(feedback_map_str_keys, f)
            print("Solver: Feedback map saved to cache.")

        print(f"Solver: Calculating best initial guess for depth {self.search_depth} and metric {self.optimization_metric}...")
        self.best_initial_guesses_by_config[(self.search_depth, self.optimization_metric)] = \
            self._find_best_guess_multi_layer(frozenset(self.possible_solutions), self.search_depth, self.optimization_metric)
        print(f"Solver: Best initial guess found: {self.best_initial_guesses_by_config[(self.search_depth, self.optimization_metric)]}")

    def _calculate_entropy(self, guess, current_possible_solutions):
        # This method is primarily for depth 1 (greedy) and min_avg_remaining, 
        # but the multi-layer evaluation will use _evaluate_guess
        pattern_counts = collections.defaultdict(int)
        for solution in current_possible_solutions:
            feedback_pattern = self.feedback_map[(guess, solution)]
            pattern_counts[feedback_pattern] += 1

        total_solutions = len(current_possible_solutions)
        if total_solutions == 0:
            return 0.0

        entropy = 0.0
        for count in pattern_counts.values():
            probability = count / total_solutions
            if probability > 0: # Avoid log(0)
                entropy -= probability * math.log2(probability)
        return entropy

    def _calculate_expected_guesses(self, current_possible_solutions_frozenset, depth):
        # Memoization check
        if current_possible_solutions_frozenset in self._expected_guesses_memo:
            return self._expected_guesses_memo[current_possible_solutions_frozenset]

        current_possible_solutions = list(current_possible_solutions_frozenset)

        # Base cases
        if len(current_possible_solutions) == 0:
            return 0 # Should not happen in a solvable game
        if len(current_possible_solutions) == 1:
            return 1 # One guess to get the last word
        
        # If depth is 0, we can't look further, so we estimate 1 + current_size/2 (heuristic)
        # Or, for simplicity, we can just return a large number to discourage this path
        if depth == 0:
            # This is a heuristic. A more accurate approach would be to use a pre-calculated
            # expected guesses for this state, or a simpler greedy approach.
            # For now, we'll use a simple heuristic or a large number to avoid infinite recursion
            # and to make it computationally feasible for deeper searches.
            # Returning len(current_possible_solutions) as a proxy for remaining guesses
            # is a common simplification for computational feasibility.
            return len(current_possible_solutions) # Heuristic: roughly how many more guesses

        min_expected_total_guesses = float('inf')

        # Iterate through all allowed guesses to find the best one
        for guess in self.allowed_guesses:
            expected_guesses_for_this_guess = 1 # The current guess itself
            
            pattern_groups = collections.defaultdict(list)
            for solution in current_possible_solutions:
                feedback_pattern = self.feedback_map[(guess, solution)]
                pattern_groups[feedback_pattern].append(solution)
            
            # Calculate weighted average of future expected guesses
            for pattern, group in pattern_groups.items():
                group_frozenset = frozenset(group)
                
                if len(group) == 0: # Should not happen
                    continue
                elif len(group) == 1: # If a guess leads to a single solution, it's solved in 1 more guess
                    expected_guesses_for_this_guess += (1 * len(group) / len(current_possible_solutions))
                else:
                    # Recursively calculate expected guesses for the next state
                    expected_guesses_from_next_state = self._calculate_expected_guesses(group_frozenset, depth - 1)
                    expected_guesses_for_this_guess += (expected_guesses_from_next_state * len(group) / len(current_possible_solutions))
            
            min_expected_total_guesses = min(min_expected_total_guesses, expected_guesses_for_this_guess)
        
        # Store in memo and return
        self._expected_guesses_memo[current_possible_solutions_frozenset] = min_expected_total_guesses
        return min_expected_total_guesses


    def _evaluate_guess(self, guess, current_possible_solutions_frozenset, depth, optimization_metric):
        current_possible_solutions = list(current_possible_solutions_frozenset)

        # Base case: if no more depth to search or only one solution left
        if depth == 0 or len(current_possible_solutions) <= 1:
            if optimization_metric == 'min_avg_guesses':
                # If we hit depth 0, we can't look further. Estimate remaining guesses.
                # This is a heuristic. A more accurate approach would be to use pre-calculated
                # expected guesses for this state, or a simpler greedy approach.
                return len(current_possible_solutions) # Heuristic: roughly how many more guesses
            else:
                return len(current_possible_solutions)

        # Group solutions by feedback pattern for the current guess
        pattern_groups = collections.defaultdict(list)
        for solution in current_possible_solutions:
            feedback_pattern = self.feedback_map[(guess, solution)]
            pattern_groups[feedback_pattern].append(solution)

        if optimization_metric == 'min_max_remaining':
            max_remaining = 0
            for pattern, group in tqdm(pattern_groups.items(), desc="Evaluating guess"):
                group_frozenset = frozenset(group)
                # Recursively evaluate the best next guess for this group
                next_best_guess = self._find_best_guess_multi_layer(group_frozenset, depth - 1, optimization_metric)
                # Evaluate the outcome of that next best guess
                outcome = self._evaluate_guess(next_best_guess, group_frozenset, depth - 1, optimization_metric)
                max_remaining = max(max_remaining, outcome)
            return max_remaining

        elif optimization_metric == 'min_avg_remaining':
            total_remaining = 0
            for pattern, group in tqdm(pattern_groups.items(), desc="Evaluating guess"):
                group_frozenset = frozenset(group)
                # Recursively evaluate the best next guess for this group
                next_best_guess = self._find_best_guess_multi_layer(group_frozenset, depth - 1, optimization_metric)
                # Evaluate the outcome of that next best guess
                outcome = self._evaluate_guess(next_best_guess, group_frozenset, depth - 1, optimization_metric)
                total_remaining += outcome * len(group)
            return total_remaining / len(current_possible_solutions) if current_possible_solutions else 0

        elif optimization_metric == 'min_avg_guesses':
            # This is the actual implementation for minimizing average guesses
            # It calls the dedicated recursive function for expected guesses
            return self._calculate_expected_guesses(current_possible_solutions_frozenset, depth)

        # Fallback for unexpected metric
        return len(current_possible_solutions)

    def _find_best_guess_multi_layer(self, current_possible_solutions_frozenset, search_depth, optimization_metric):
        current_possible_solutions = list(current_possible_solutions_frozenset)

        if len(current_possible_solutions) == 1:
            return current_possible_solutions[0]
        if not current_possible_solutions:
            return random.choice(self.allowed_guesses) # Fallback

        best_score = float('inf') # We want to minimize remaining solutions/guesses
        best_guess = None

        # For multi-layer search, we consider all allowed guesses as candidates
        # This is the most computationally intensive part
        candidate_guesses = self.allowed_guesses # Or a subset for optimization

        for guess in candidate_guesses:
            score = self._evaluate_guess(guess, current_possible_solutions_frozenset, search_depth, optimization_metric)
            if score < best_score:
                best_score = score
                best_guess = guess
        
        # Fallback if no best guess found (e.g., all scores are inf or 0)
        if best_guess is None:
            # If current_possible_solutions is not empty, pick one of them
            if current_possible_solutions:
                return current_possible_solutions[0]
            else:
                return random.choice(self.allowed_guesses) # Final fallback

        return best_guess

    def get_next_guess(self, guess_history):
        # Use pre-calculated initial guess if available and it's the first turn
        if not guess_history:
            config_key = (self.search_depth, self.optimization_metric)
            if config_key in self.best_initial_guesses_by_config:
                return self.best_initial_guesses_by_config[config_key]
            else:
                # If not pre-calculated, calculate it now (should ideally be pre-calculated)
                print(f"Warning: Initial guess for depth {self.search_depth} and metric {self.optimization_metric} not pre-calculated. Calculating now...")
                self.best_initial_guesses_by_config[config_key] = \
                    self._find_best_guess_multi_layer(frozenset(self.possible_solutions), self.search_depth, self.optimization_metric)
                return self.best_initial_guesses_by_config[config_key]

        # Filter possible solutions based on guess history
        current_possible_solutions_list = list(self.possible_solutions)
        for prev_guess, prev_feedback in guess_history:
            current_possible_solutions_list = [ 
                solution for solution in current_possible_solutions_list 
                if self.feedback_map[(prev_guess, solution)] == prev_feedback
            ]
        
        current_possible_solutions_frozenset = frozenset(current_possible_solutions_list)

        # If only one solution left, return it
        if len(current_possible_solutions_list) == 1:
            return current_possible_solutions_list[0]
        
        # If no solutions left (shouldn't happen with correct logic), return a default or raise error
        if not current_possible_solutions_list:
            print("Warning: No possible solutions left. This indicates an error in logic or word lists.")
            return random.choice(self.allowed_guesses) # Fallback

        # For subsequent guesses, use the multi-layer search with the configured depth and metric
        # This will be computationally expensive for depth > 1
        return self._find_best_guess_multi_layer(current_possible_solutions_frozenset, self.search_depth, self.optimization_metric)
