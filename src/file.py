import json
from time import perf_counter

import psycopg2
import redis

from main import does_word_fit, create_pattern_chart, compare_word_with_key

redis_patterns = redis.Redis(host='localhost', port=6379, db=1)

conn = psycopg2.connect(
	host="localhost",
	port=5432,
	database="wordle",
	user="wordle",
	password="wordle"
)
cur = conn.cursor()

top_pick = 'kalio'
guessed_pattern = (0, 0, 0, 0, 0)

with open("/Users/filip/Developer/Python/WordleAlg/src/data/words.json") as file:
	data = json.load(file)
	words_available = data['slowa']

new_words = []
for word in words_available:
	if does_word_fit(word, guessed_pattern, top_pick):
		new_words.append(word)
n = len(new_words)
print(len(new_words))

new_entropies = {}

word = new_words[0]
print(word)

start = perf_counter()
s1 = set(words_available)

pattern_distribution = redis_patterns.hgetall(word)
pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}

for pattern, word_list in pattern_distribution.items():
	s2 = set(word_list)
	s_temp = s2 - s1
	pattern_distribution[pattern] = list(s2 - s_temp)
score = create_pattern_chart(word, words_available, pattern_distribution)

end = perf_counter()
print(f'Redis all search: {(end - start) * 1000:0.0f} ms.')

start = perf_counter()
s1 = set(words_available)

pattern_distribution = {}
for ch_word in new_words:
	pattern = compare_word_with_key(ch_word, word)
	if pattern not in pattern_distribution:
		pattern_distribution[pattern] = []
	pattern_distribution[pattern].append(ch_word)

# pattern_distribution = redis_patterns.hgetall(word)
# pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}

for pattern, word_list in pattern_distribution.items():
	s2 = set(word_list)
	s_temp = s2 - s1
	pattern_distribution[pattern] = list(s2 - s_temp)
score = create_pattern_chart(word, words_available, pattern_distribution)

end = perf_counter()
print(f'Redis all search: {(end - start) * 1000:0.0f} ms.')


def recalculate_entropies():
	new_entropies = {}
	s1 = set(words_available)
	
	for word in words_available[:1]:
		pattern_distribution = redis_patterns.hgetall(word)
		# print(pattern_distribution)
		pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}
		for pattern, word_list in pattern_distribution.items():
			s2 = set(word_list)
			s_temp = s2 - s1
			pattern_distribution[pattern] = list(s2 - s_temp)
		score = create_pattern_chart(word, words_available, pattern_distribution)
		new_entropies[word] = score
	
	new_entropies = sorted(new_entropies.items(), key=lambda x: x[1], reverse=True)
	return new_entropies

# recalculate_entropies()
# start = perf_counter()
# words_array = ['abbac-%', 'acani-%', 'adasi-%']
# sql = f"""select checking_word_pattern, key_words from pattern_table where checking_word_pattern like any (ARRAY[{new_words}]) group by checking_word_pattern;"""
# cur.execute(sql)
# cur.fetchall()
# end = perf_counter()
# print(f'Postgres all search: {(end - start) * 1000:0.0f} ms. average {(end - start) * 1000 / n:0.0f} ms')
