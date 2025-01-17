import numpy as np
import collections

def merge(test):
    word = ''
    for x in test:
        word += x
    return str(word)

def split(string):
    return np.array([char for char in string], dtype=str)

def count_occurrences(letter, list):
    return collections.Counter(list)[letter]