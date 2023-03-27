import json
import random
import redis
import psycopg2

from main import compare_word_with_key, does_word_fit, create_pattern_chart


redis_sorted = redis.Redis(host='localhost', port=6379, db=0)
redis_patterns = redis.Redis(host='localhost', port=6379, db=1)

conn = psycopg2.connect(
	host="localhost",
	port=5432,
	database="wordle",
	user="wordle",
	password="wordle"
)
cur = conn.cursor()


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


class Bot:
	
	def __init__(self, words):
		self.words_available = words
		self.previous_pattern = []
		self.sql_words = []
		self.redis_words = []
	
	def load_word_lists(self):
		with open("data/extended_words.json") as file:
			data = json.load(file)
			self.sql_words = data['slowa']
		
		with open("data/short_words.json") as file:
			data = json.load(file)
			self.redis_words = data['slowa']
	
	def recalculate_entropies(self):
		new_entropies = {}
		s1 = set(self.words_available)
		for word in self.words_available:
			pattern_distribution = redis_patterns.hgetall(word)
			pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}
			for pattern, word_list in pattern_distribution.items():
				s2 = set(word_list)
				s_temp = s2 - s1
				pattern_distribution[pattern] = list(s2 - s_temp)
			score = create_pattern_chart(word, self.words_available, pattern_distribution)
			new_entropies[word] = score
		
		new_entropies = sorted(new_entropies.items(), key=lambda x: x[1], reverse=True)
		return new_entropies
	
	def choose_word(self):
		if not wordle.can_play():
			return
		if not self.previous_pattern:
			top_scores = redis_sorted.zrevrange('firstEntropy', 0, 9)
			top_pick = top_scores[0].decode('utf-8')
			print(top_pick)
			guessed_pattern = wordle.turn(top_pick)
			print(guessed_pattern)
			self.previous_pattern.append(guessed_pattern)
			
			new_words = []
			for word in self.words_available:
				if does_word_fit(word, guessed_pattern, top_pick):
					new_words.append(word)
			print(len(new_words), "remaining", "\n")
			self.words_available = new_words
			return
		else:
			# print(self.words_available)
			entropies = self.recalculate_entropies()
			top_pick = entropies[0][0]
			print(top_pick)
			guessed_pattern = wordle.turn(top_pick)
			print(guessed_pattern)
			self.previous_pattern.append(guessed_pattern)
			
			new_words = []
			for word in self.words_available:
				if does_word_fit(word, guessed_pattern, top_pick):
					new_words.append(word)
			print(len(new_words), "remaining", "\n")
			self.words_available = new_words
			
			return
			

if __name__ == '__main__':
	wordle = Game()
	wordle.load_words('words.json')
	wordle.start()
	wordle.key_word = 'metka'
	bot = Bot(wordle.words)
	
	# new_words = wordle.words
	bot.choose_word()
	bot.choose_word()
	# bot.choose_word()
	# bot.choose_word()
	# bot.choose_word()
	# bot.choose_word()
	# while wordle.can_play():
	# 	if len(wordle.ties) == 0:
	# 		bot.choose_word()
	# 		
	# 	else:
	# 		# top_scores = redis_sorted.zrevrange('entropy', 0, 4)
	# 		# top_scores = [word.decode('utf-8').lower() for word in top_scores]
	# 		# print(top_scores)
	# 		# pattern = wordle.turn(top_scores[0])
	# 		# print(pattern)
	# 		# new_words = simulate_bot(new_words, pattern, top_scores[0])
	# 		# print(len(new_words))
	# 		wordle.lost = True
