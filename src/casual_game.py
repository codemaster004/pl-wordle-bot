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


class Bot:
	
	def __init__(self, words):
		self.words_available = words
		self.all_words = words
		self.previous_pattern = []
		self.sql_words = []
		self.redis_words = []
	
	def load_word_lists(self):
		with open("/Users/filip/Developer/Python/WordleAlg/src/data/words.json") as file:
			data = json.load(file)
			self.sql_words = data['slowa']
		
		with open("/Users/filip/Developer/Python/WordleAlg/src/data/words.json") as file:
			data = json.load(file)
			self.redis_words = data['slowa']
	
	def recalculate_entropies(self):
		new_entropies = {}
		s1 = set(self.words_available)
		# print(self.words_available)
		for word in self.all_words:
			
			# pattern_distribution = redis_patterns.hgetall(word)
			# pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}
			
			pattern_distribution = {}
			for ch_word in self.words_available:
				if ch_word not in s1:
					continue
				pattern = compare_word_with_key(ch_word, word)
				if pattern not in pattern_distribution:
					pattern_distribution[pattern] = []
				pattern_distribution[pattern].append(ch_word)
			
			# for pattern, word_list in pattern_distribution.items():
			# 	s2 = set(word_list)
			# 	s_temp = s2 - s1
			# 	pattern_distribution[pattern] = list(s2 - s_temp)
			score = create_pattern_chart(word, self.words_available, pattern_distribution)
			new_entropies[word] = score
		
		new_entropies = sorted(new_entropies.items(), key=lambda x: x[1], reverse=True)
		return new_entropies
	
	def fetch_postgres_list(self):
		cur.execute('select word from saved_words')
		words = cur.fetchall()
		words = [word[0] for word in words]
		return words
	
	def fetch_redis_list(self):
		words = redis_patterns.keys('*')
		words = [word.decode('utf-8').lower() for word in words]
		return words
	
	def fetch_possible_answers_postgres(self, word, pattern):
		cur.execute(f"select key_words from pattern_table where checking_word_pattern = '{word}-{str(pattern)}' limit 1;")
		result = cur.fetchall()
		for res in result:
			words = json.loads(json.loads(res[0]))
			return words
	
	def fetch_possible_answers_redis(self, word, pattern):
		words = redis_patterns.hget(word, str(pattern))
		if not words:
			return []
		words = json.loads(words)
		return words
	
	def play_word(self, guess_word, pattern):
		self.previous_pattern.append((guess_word, pattern))
		
		new_words = self.fetch_possible_answers_redis(guess_word, pattern)
		if not new_words:
			new_words = self.fetch_possible_answers_postgres(guess_word, pattern)

		s1 = set(self.words_available)
		s2 = set(new_words)
		s_temp = s1 - s2
		
		self.words_available = list(s1 - s_temp)
		print(self.words_available[:10])
		print(len(self.words_available), "remaining", "\n")
		
		top_picks = self.choose_word()
		
		return sorted(self.words_available)[:10], len(self.words_available), top_picks
	
	def choose_word(self):
		if not self.previous_pattern:
			top_picks = redis_sorted.zrevrange('firstEntropy', 0, 19, withscores=True)
			
			print([(word[0].decode('utf-8'), word[1]) for word in top_picks])
			return top_picks
		else:
			# print(self.words_available[:29])
			entropies = self.recalculate_entropies()
			top_picks = entropies[:29]
			
			print(top_picks)
			return top_picks


if __name__ == '__main__':
	with open('/Users/filip/Developer/Python/WordleAlg/src/data/words.json') as file:
		data = json.load(file)
		all_words = data['slowa']
	
	bot = Bot(all_words)
	bot.load_word_lists()
	bot.choose_word()
	while True:
		print()
		print("What word did you play?")
		word = input("Word: ")
		
		print("What pattern turned out?")
		temp_pattern = input("Pattern: ")
		pattern = tuple([int(n) for n in list(temp_pattern)])
		
		bot.play_word(word, pattern)


"""
TODO: Check key: elita, [soria, celny, mężuś]
[00000, 00101, 01000]
"""
