import numpy as np
import json
import random
import time

with open("data/answers.json") as file:
	words = json.load(file)['slowa']
	w1 = words[:10]
	w2 = w1[:]
	random.shuffle(w2)

print(len(w1), len(w2))
print(w1[:2], w2[:2])


def convert_words_to_numbers(words):
	"""
	For given list of words. Iterates on words and letters, to convert each character into its id in unicode.
	:param words: list of words
	:return: numpy array of unicode char number ids
	"""
	return np.array([[ord(c) for c in w] for w in words], dtype=np.uint16)


arr1, arr2 = map(convert_words_to_numbers, (w1, w2))

# start = time.perf_counter()
# end = time.perf_counter()
# print(f'Done in: {(end - start)*1_000_000:0.0f} us')

green_comparison = (arr1 == arr2)


green = np.where(green_comparison, 2, 0)
arr1 = np.where(green_comparison, 0, arr1)
print(green)
print(arr1)

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = np.array([[1, 2, 3], [4, 5, 6], [8, 7, 9]])
c = np.where(np.in1d(a[:, 0], b), b[:, 0], -1)
# print(c)

# print(np.zeros((5, 5, 2, 2)))
