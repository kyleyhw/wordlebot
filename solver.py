import collections
import math
import random
import sys
import json
import os
import pickle
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
    def __init__(self, word_list_manager_instance, search_depth=1, optimization_metric='min_avg_remaining'):
        self.word_list_manager = word_list_manager_instance
        self.allowed_guesses = self.word_list_manager.get_allowed_guesses()
        self.possible_solutions = self.word_list_manager.get_possible_solutions()
        self.search_depth = search_depth
        self.optimization_metric = optimization_metric
        self.feedback_map = {}
        self.best_initial_guesses_by_config = {}
        self._expected_guesses_memo = {}

        if self.optimization_metric not in ['min_max_remaining', 'min_avg_remaining', 'min_avg_guesses']:
            raise ValueError("optimization_metric must be 'min_max_remaining', 'min_avg_remaining', or 'min_avg_guesses'")

        feedback_map_cache_file = "feedback_map.pkl"
        if os.path.exists(feedback_map_cache_file):
            print("Solver: Loading feedback map from cache...")
            with open(feedback_map_cache_file, 'rb') as f:
                self.feedback_map = pickle.load(f)
            print("Solver: Feedback map loaded from cache.")
        else:
            raise FileNotFoundError(f"Feedback map not found at {feedback_map_cache_file}. Please run generate_feedback_map.py first.")

        print(f"Solver: Calculating best initial guess for depth {self.search_depth} and metric {self.optimization_metric}...")
        # Store the list of (guess, score) tuples
        self.best_initial_guesses_by_config[(self.search_depth, self.optimization_metric)] = \
            self._find_best_guess_multi_layer(frozenset(self.possible_solutions), self.search_depth, self.optimization_metric, num_recommendations=1, show_progress=True)
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
            for pattern, group in pattern_groups.items():
                group_frozenset = frozenset(group)
                # Recursively evaluate the best next guess for this group
                next_best_guess = self._find_best_guess_multi_layer(group_frozenset, depth - 1, optimization_metric)
                # Evaluate the outcome of that next best guess
                outcome = self._evaluate_guess(next_best_guess, group_frozenset, depth - 1, optimization_metric)
                max_remaining = max(max_remaining, outcome)
            return max_remaining

        elif optimization_metric == 'min_avg_remaining':
            total_remaining = 0
            for pattern, group in pattern_groups.items():
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

    def _find_best_guess_multi_layer(self, current_possible_solutions_frozenset, search_depth, optimization_metric, num_recommendations=1, show_progress=False):
        current_possible_solutions = list(current_possible_solutions_frozenset)

        if len(current_possible_solutions) == 1:
            return [(current_possible_solutions[0], 0.0)] # Return as a list of (guess, score)
        if not current_possible_solutions:
            return [(random.choice(word_list_manager.get_allowed_guesses()), float('inf'))] # Fallback, return with high score

        all_candidate_scores = []

        candidate_guesses = self.allowed_guesses

        # Apply tqdm only if show_progress is True
        if show_progress:
            iterable_guesses = tqdm(candidate_guesses, desc="Calculating best initial guess")
        else:
            iterable_guesses = candidate_guesses

        for guess in iterable_guesses:
            score = self._evaluate_guess(guess, current_possible_solutions_frozenset, search_depth, optimization_metric)
            all_candidate_scores.append((score, guess))
        
        # Sort by score (ascending) and take the top num_recommendations
        all_candidate_scores.sort(key=lambda x: x[0])
        
        # Return a list of (guess, score) tuples
        return [(guess, score) for score, guess in all_candidate_scores[:num_recommendations]]

    def get_next_guess(self, guess_history, num_recommendations=1):
        # Use pre-calculated initial guess if available and it's the first turn
        if not guess_history:
            config_key = (self.search_depth, self.optimization_metric)
            if config_key in self.best_initial_guesses_by_config:
                # If num_recommendations is 1, we can use the cached single best guess
                if num_recommendations == 1:
                    # self.best_initial_guesses_by_config[config_key] already stores a list of (guess, score) tuples
                    # We just need the first one if num_recommendations is 1
                    return [self.best_initial_guesses_by_config[config_key][0]]
                else:
                    # If we need more than 1 recommendation, we need to re-calculate
                    # This will overwrite the single best guess in cache if it was stored as such
                    print(f"Warning: Initial guess for depth {self.search_depth} and metric {self.optimization_metric} needs re-calculation for multiple recommendations.")
                    recommendations = self._find_best_guess_multi_layer(frozenset(self.possible_solutions), self.search_depth, self.optimization_metric, num_recommendations, show_progress=True)
                    self.best_initial_guesses_by_config[config_key] = recommendations # Cache the list of recommendations
                    return recommendations
            else:
                # If not pre-calculated, calculate it now (should ideally be pre-calculated)
                print(f"Warning: Initial guess for depth {self.search_depth} and metric {self.optimization_metric} not pre-calculated. Calculating now...")
                recommendations = self._find_best_guess_multi_layer(frozenset(self.possible_solutions), self.search_depth, self.optimization_metric, num_recommendations, show_progress=True)
                # Cache the list of recommendations
                self.best_initial_guesses_by_config[config_key] = recommendations
                return recommendations

        # Filter possible solutions based on guess history
        current_possible_solutions_list = list(self.possible_solutions)
        for prev_guess, prev_feedback in guess_history:
            filtered_solutions = []
            for solution in current_possible_solutions_list:
                if self.feedback_map[(prev_guess, solution)] == prev_feedback:
                    filtered_solutions.append(solution)
            current_possible_solutions_list = filtered_solutions
            current_possible_solutions_frozenset = frozenset(current_possible_solutions_list)

        # If only one solution left, return it
        if len(current_possible_solutions_list) == 1:
            return [(current_possible_solutions_list[0], 0.0)] # Return as a list of (guess, score)
        
        # If no solutions left (shouldn't happen with correct logic), return a default or raise error
        if not current_possible_solutions_list:
            print("Warning: No possible solutions left. This indicates an error in logic or word lists.")
            return [(random.choice(word_list_manager.get_allowed_guesses()), float('inf'))] # Fallback

        # For subsequent guesses, use the multi-layer search with the configured depth and metric
        return self._find_best_guess_multi_layer(current_possible_solutions_frozenset, self.search_depth, self.optimization_metric, num_recommendations, show_progress=True)
