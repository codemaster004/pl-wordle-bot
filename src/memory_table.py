import pandas as pd
import json
import itertools
import math
from time import perf_counter
import redis
import psycopg2

from main import compare_word_with_key

conn = psycopg2.connect(
	host="localhost",
	port=5432,
	database="wordle",
	user="wordle",
	password="wordle"
)
cur = conn.cursor()

redis_patterns = redis.Redis(host='localhost', port=6379, db=1)

with open("data/extended_words.json") as file:
	data = json.load(file)
	extended_words = data['slowa']

with open("data/short_words.json") as file:
	data = json.load(file)
	short_words = data['slowa']

with open("data/words.json") as file:
	data = json.load(file)
	full_words = data['slowa']


def initial_table_creation():
	cur.execute('''CREATE TABLE pattern_table (checking_word_pattern TEXT PRIMARY KEY, key_words TEXT)''')
	cur.execute('''CREATE TABLE saved_words (word TEXT PRIMARY KEY)''')
	conn.commit()


def add_word_patterns_redis(data_dict):
	redis_patterns.hset(data_dict['key'], mapping=data_dict['patterns'])


def calc_patters_for_word(checking_word, full_words):
	# Generating Empty template with all patterns as keys
	temp_dict = {
		'key': checking_word,
		'patterns': {str(pattern): [] for pattern in list(itertools.product(range(3), repeat=len(checking_word)))}
	}
	
	for key_word in full_words:
		generated_pattern = compare_word_with_key(key_word, checking_word)
		temp_dict['patterns'][str(generated_pattern)].append(key_word)
	
	for pattern in temp_dict['patterns']:
		temp_dict['patterns'][pattern] = json.dumps(temp_dict['patterns'][pattern])
	
	return temp_dict


def calc_all_patterns(words, full_words):
	calculate_words = redis_patterns.keys('*')
	calculate_words = [word.decode('utf-8').lower() for word in calculate_words]
	missing_words = list(set(words) - set(calculate_words))
	missing_words.sort()
	
	print(len(missing_words), "are missing!")
	for checking_word in missing_words:
		pattern_dict = calc_patters_for_word(checking_word, full_words)
		
		add_word_patterns_redis(pattern_dict)


def add_word_patterns_sql(data_dict):
	key = data_dict['key']
	word_patterns = {f'{key}-{p}': json.dumps(w) for p, w in data_dict['patterns'].items()}
	sql_formatted_patterns = list(zip(word_patterns.keys(), word_patterns.values()))
	cur.executemany('''INSERT INTO pattern_table (checking_word_pattern, key_words) VALUES (%s, %s);''', sql_formatted_patterns)
	cur.execute(f"""INSERT INTO saved_words VALUES ('{key}');""")
	conn.commit()
	print(f'{key} added!')


def calc_remaining_patterns(words, full_words):
	cur.execute('''SELECT word FROM saved_words;''')
	calculate_words = [word[0] for word in cur.fetchall()]
	missing_words = list(set(words) - set(calculate_words))
	missing_words.sort()
	
	print(len(missing_words), "are missing!")
	for checking_word in missing_words:
		pattern_dict = calc_patters_for_word(checking_word, full_words)
		
		add_word_patterns_sql(pattern_dict)


if __name__ == '__main__':
	initial_table_creation()
	calc_all_patterns(short_words, full_words)
	calc_remaining_patterns(extended_words, full_words)
	
	cur.close()
	conn.close()
# start = perf_counter()
# calc_all_patterns(words)
# end = perf_counter()
# print(f"Patterns generated in {(end - start) * 1000:0.0f} ms")


# df = pd.DataFrame(memory_table)

# Print the DataFrame
# print(df)
# df.to_csv('data.csv')
# filtered_df = df[df['oc'] == '(0, 1)']['oc']
# print(len(filtered_df))

# check_word = 'abo'
# 
# entropy = 0
# possible_patterns = list(itertools.product(range(3), repeat=len(check_word)))
# # pattern_chart = {'key': check_word, 'patterns': {}, 'entropy': 0}
# for pattern in possible_patterns:
# 	n = len(df[df[check_word] == str(pattern)][check_word])
# 	
# 	probability = n / len(words)
# 	if probability != 0:
# 		information = math.log2(1 / probability)
# 		entropy += probability * information
# # pattern_chart['patterns'][str(pattern)] = probability
# 
# print(entropy)
# for probability in pattern_chart['patterns'].values():
# 	information = math.log2(1 / probability)
# 	entropy += probability * information

# pattern_chart['entropy'] = entropy
