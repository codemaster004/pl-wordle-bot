import pandas as pd
import json
import itertools
import math
import sqlite3
from time import perf_counter
import redis
import wolframclient

from main import compare_word_with_key

conn = sqlite3.connect('patterns.db')
c = conn.cursor()

redis_patterns = redis.Redis(host='localhost', port=6379, db=1)


with open("data/words.json") as file:
	data = json.load(file)
	words = data['slowa']
	

def initial_table_creation():
	create_table_sql = '''CREATE TABLE pattern_table
	(words_combination TEXT UNIQUE, checking_word CHAR(5), target_word CHAR(5), pattern TEXT);'''
	# c.execute(create_table_sql)
	# conn.commit()
	

def add_word_patterns(data_dict):
	redis_patterns.hset(data_dict['key'], mapping=data_dict['patterns'])


# initial_table_creation()

def calc_all_patterns(words):
	calculate_words = redis_patterns.keys('*')
	calculate_words = [word.decode('utf-8').lower() for word in calculate_words]
	missing_words = list(set(words) - set(calculate_words))
	missing_words.sort(reverse=True)
	print(len(missing_words), "are missing!")
	for checking_word in missing_words:
		temp_dict = {
			'key': checking_word,
			'patterns': {str(pattern): [] for pattern in list(itertools.product(range(3), repeat=len(checking_word)))}
		}
		for key_word in words:
			generated_pattern = compare_word_with_key(key_word, checking_word)
			temp_dict['patterns'][str(generated_pattern)].append(key_word)
		
		for pattern in temp_dict['patterns']:
			temp_dict['patterns'][pattern] = json.dumps(temp_dict['patterns'][pattern])
		
		add_word_patterns(temp_dict)


# start = perf_counter()
calc_all_patterns(words)
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
