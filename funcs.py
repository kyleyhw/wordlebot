import numpy as np

def merge(test):
    word = ''
    for x in test:
        word += x
    return str(word)

def split(string):
    return np.array([char for char in string], dtype=str)

# def green_indices(solution, guess):
#     indices = []
#     for i, (solution_element, guess_element) in enumerate(zip(solution, guess)):
#         if solution_element == guess_element:
#             indices.append(i)
#     return np.array(indices)
#
# def yellow_indices(solution, guess):
#     letters = np.intersect1d(solution, guess)
#     indices = np.concatenate([np.asarray(guess == letter).nonzero()[0] for letter in letters])
#
#     if len(set(guess)) != len(guess):
#         letter_occurrences_in_guess = np.asarray([np.count_nonzero(guess == letter) for letter in letters])
#
#
#     return indices
#
# solution = split('abcbf')
# guess = split('abcae')
#
# green_test = green_indices(solution, guess)
# yellow_test = yellow_indices(solution, guess)
#
# print(green_test)
# print(yellow_test)