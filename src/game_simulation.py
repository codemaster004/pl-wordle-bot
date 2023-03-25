import json
import random
import redis

from main import compare_word_with_key, does_word_fit


redis_sorted = redis.Redis(host='localhost', port=6379, db=3)


class Game:
	def __init__(self):
		self.key_word = None
		self.words = []
		self.won = False
		self.lost = False
		self.ties = []
	
	def load_words(self, file_name):
		with open(f'data/{file_name}', "r") as f:
			data = json.load(f)
			self.words = data['slowa']
	
	def start(self):
		self.key_word = random.choice(self.words)
		self.won = False
		self.lost = False
		self.ties = []
	
	def can_play(self):
		return not (self.won or self.lost)
	
	def turn(self, guessing_word):
		if self.won or self.lost:
			return
		
		if guessing_word == self.key_word:
			self.won = True
			return [2, 2, 2, 2, 2]
		
		pattern = compare_word_with_key(self.key_word, guessing_word)
		self.ties.append((pattern, guessing_word))
		
		if len(self.ties) >= 6:
			self.lost = True
		
		return pattern


def simulate_bot(words, pattern, check_word):
	words_passed = []
	for word in words:
		# Check if word from word list matches pattern build on the check_word
		if does_word_fit(word, pattern, check_word):
			words_passed.append(word)
	
	return words_passed


if __name__ == '__main__':
	wordle = Game()
	wordle.load_words('simple_word.json')
	wordle.start()
	
	new_words = wordle.words
	while wordle.can_play():
		top_scores = redis_sorted.zrevrange('entropy', 0, 4)
		top_scores = [word.decode('utf-8').lower() for word in top_scores]
		print(top_scores)
		pattern = wordle.turn(top_scores[0])
		print(pattern)
		new_words = simulate_bot(new_words, pattern, top_scores[0])
		print(len(new_words))
		wordle.lost = True
