import json
import random
import time
import itertools
import math


def compare_word_with_key(key, word):
	"""
	Function for given current Key Word and user guessed Word returns the color pattern representing guess coverage
	
	:param key: Key word that user tries to guess
	:type key: str
	
	:param word: 5 letter guess word given by player
	:type word: str
	
	:return: Returns patter for coverage of given word on key
	:rtype: list[int]
	"""
	temp_key = list(key)

	pattern = [0] * 5
	
	orange_char = []
	for i, char in enumerate(word):
		# Check if letter exists anywhere in the key word
		if char in temp_key:
			
			# Check for Green letters
			if temp_key[i] == char:
				pattern[i] = 2
				temp_key[i] = None  # Because of double letter we remove Green ones to enable easy checks later
			
			# Check for orange letters. Because of a need to handle double letters differently those will be dealt with later
			orange_char.append((i, char))
	
	# After checking the rest of the word we can check if exists
	for i, char in orange_char:
		# Now we check if letter still exists inside the word
		if char in temp_key:
			pattern[i] = 1
			temp_key[temp_key.index(char)] = None  # for safety lets remove it if triple letters happen
	
	return pattern


if __name__ == '__main__':
	# key = 'mścić'
	# word = 'cucić'
	# patttern = check_word(word, key)
	# v = list(zip(patttern, word))
	# print(v)
	# print(does_word_fit('mścić', v))
	
	# with open("data.json") as file:
	# 	data = json.load(file)
	# 	words = data['slowa'][:]
	# 
	# 	start = time.perf_counter()
	# 	create_patttern_chart('debil', words)
	# 	end = time.perf_counter()
	# 	print(f"Entropy checked in {(end - start) * 1000:0.0f} ms")
	
	# for word in words:
	# 	z = zip([1, 0, 0, 0, 1], 'dynia')
	# 	if does_word_fit(word, z):
	# 		z = zip([0, 2, 2, 0, 0], 'sadło')
	# 		if does_word_fit(word, z):
	# 			z = zip([0, 2, 2, 2, 2], 'badać')
	# 			if does_word_fit(word, z):
	# 				print(word, end=' ')
	
	# n = 2_000
	# start = time.perf_counter()
	# for _ in range(n):
	# 	does_word_fit('abide', [0, 0, 1, 0, 1], 'speed')
	# 	does_word_fit('erase', [1, 0, 1, 1, 0], 'speed')
	# 	does_word_fit('steal', [2, 0, 2, 0, 0], 'speed')
	# 	does_word_fit('crepe', [0, 1, 2, 1, 0], 'speed')
	# end = time.perf_counter()
	# print(f"{n} Patterns checked in {(end - start) * 1000:0.0f} ms")
	pass
