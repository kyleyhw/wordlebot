import numpy as np

from funcs import split

class solver:
    def __init__(self, word_list):
        self.word_list = np.array([split(word) for word in word_list])

    def _get_letters_and_indices(self, color, guess, colors):
        indices = np.where(colors == color)[0]
        letters = guess[indices]
        return letters, indices

    def _update_greens(self, green_letters, green_indices):
        if len(green_letters) == 0:
            return
        reject_indices = []
        for i, word in enumerate(self.word_list):
            if not np.array_equal(word[green_indices], green_letters):
                reject_indices.append(i)
        if len(reject_indices) > 0:
            self.word_list = np.delete(self.word_list, reject_indices, axis=0)

    def _update_yellows(self, yellow_letters, yellow_indices, green_letters, green_indices): # messy, but doesn't seem possible without green indices since green letters must be ignored when checking for yellow
        if len(yellow_letters) == 0:
            return
        reject_indices = []
        for i, word in enumerate(self.word_list):
            # if not ((len(np.intersect1d(yellow_letters, word)) == len(yellow_letters)) and (len(np.intersect1d(yellow_letters, word[yellow_indices])) == 0)):
            reject = False
            for j, yellow_letter in enumerate(yellow_letters):
                yellow_letters_in_solution_indices = np.where(word == yellow_letter)[0]
                for green_index in green_indices:
                    yellow_letters_in_solution_indices = np.delete(yellow_letters_in_solution_indices, np.where(yellow_letters_in_solution_indices == green_index))
                print(word, yellow_letters_in_solution_indices)
                if not ((yellow_letter in np.delete(word, np.concatenate((green_indices, yellow_letters_in_solution_indices[:j])))) and (yellow_letter not in word[yellow_indices])):
                    reject = True
            if reject:
                reject_indices.append(i)
        if len(reject_indices) > 0:
            self.word_list = np.delete(self.word_list, reject_indices, axis=0)


    def update_possibilities(self, guess, colors):
        guess = split(guess)
        colors = split(colors)

        green_letters, green_indices = self._get_letters_and_indices('g', guess, colors)
        self._update_greens(green_letters, green_indices)
        print(self.word_list)

        yellow_letters, yellow_indices = self._get_letters_and_indices('y', guess, colors)
        print(yellow_letters, yellow_indices)
        self._update_yellows(yellow_letters, yellow_indices, green_letters, green_indices)
        print(self.word_list)



word_list = np.genfromtxt('data/wordle_allowed_guesses_unsorted.txt', dtype=str)

solver(word_list).update_possibilities('aaaaa', 'gybby')