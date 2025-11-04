from funcs import split, count_occurrences

# game format: 5 letter word followed by 5 letter string, each char in string contains 'b' or 'y' or 'g' for black or yellow or green respectively

class game:
    def __init__(self, solution):
        self.solution = split(solution)

    def enter(self, guess):
        colors = split('bbbbb')
        guess = split(guess)
        green_letters = []
        for i, letter in enumerate(guess):
            if letter == self.solution[i]:
                colors[i] = 'g'
                green_letters.append(letter)

        # Create a mutable list from the solution to mark letters as used
        solution_copy = list(self.solution)

        # First pass: Check for green letters
        for i, letter in enumerate(guess):
            if letter == solution_copy[i]:
                colors[i] = 'g'
                solution_copy[i] = None  # Mark as used

        # Second pass: Check for yellow and black letters
        for i, letter in enumerate(guess):
            if colors[i] != 'g':  # Only check if not already marked green
                if letter in solution_copy:
                    colors[i] = 'y'
                    solution_copy[solution_copy.index(letter)] = None  # Mark as used
                else:
                    colors[i] = 'b'
        return "".join(colors)