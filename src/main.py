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
	:rtype: tuple[int]
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
	
	return tuple(pattern)


def does_word_fit(check_word, pattern_list, pattern_word):
	"""
	Given a check_word determines if it matches given pattern_list in combination with pattern_word
	
	:param check_word: Currently, checking word if matches the pattern
	:type check_word: str
	
	:param pattern_list: Color pattern showing if a letter exists somewhere ant exactly this position or doesn't exist
	:type pattern_list: tuple[int]
	
	:param pattern_word: Connected with a pattern is a word it was generated on
	:type pattern_word: str
	
	:return: If the check_word matches the given pattern
	:rtype: bool
	"""
	
	gray = []
	orange = []
	green = []
	# Break up pattern letters into appropriate colors
	for index, pattern in enumerate(pattern_list):
		match pattern:
			case 2:
				# Green require letter and position it is on
				green.append((index, pattern_word[index]))
			case 1:
				# Orange require letter and position it is Not on
				orange.append((index, pattern_word[index]))
			case _:
				# Otherwise it is gray so only letter matters
				gray.append(pattern_word[index])
	
	temp = list(check_word)
	# WARNING: Order in witch you check letter color matters
	# First check if Green letter exists on exact position
	for i, char in green:
		if temp[i] != char:
			return False
		else:
			temp[i] = None  # remove it because of need to check double letters
	
	# Second check Orange if letter exists and Not on given position
	for i, char in orange:
		if char not in temp:
			return False
		
		index = temp.index(char)
		if i == index:
			return False
		else:
			temp[index] = None  # remove it because of need to check double letters
	
	# Last check if gray letters don't exist in word
	for char in gray:
		if char in temp:
			return False
	
	return True


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
