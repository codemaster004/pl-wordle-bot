import pandas as pd
import json
import itertools
import math
import sqlite3
from time import perf_counter

from main import compare_word_with_key

conn = sqlite3.connect('patterns.db')
c = conn.cursor()

redis_distribution = redis.Redis(host='localhost', port=6379, db=5)


with open("data/words.json") as file:
	data = json.load(file)
	words = data['slowa']
	

def initial_table_creation():
	create_table_sql = '''CREATE TABLE pattern_table
	(words_combination TEXT UNIQUE, checking_word CHAR(5), target_word CHAR(5), pattern TEXT);'''
	# c.execute(create_table_sql)
	# conn.commit()
	

def add_word_patterns(pattern_data):
	try:
		c.executemany('INSERT INTO pattern_table VALUES (?, ?, ?, ?)', pattern_data)
		conn.commit()
	except sqlite3.IntegrityError:
		print('Those values are already added')


# initial_table_creation()

def calc_all_patterns():
	for checking_word in words:
		temp_table = {
			'words_combination': [],
			'checking_word': [],
			'target_word': [],
			'pattern': []
		}
		for key_word in words:
			generated_pattern = compare_word_with_key(key_word, checking_word)
			temp_table['words_combination'].append(f'{checking_word}-{key_word}')
			temp_table['checking_word'].append(checking_word)
			temp_table['target_word'].append(key_word)
			temp_table['pattern'].append(str(generated_pattern))
		
		transformed_table = list(zip(temp_table['checking_word'], temp_table['target_word'], temp_table['pattern']))
		add_word_patterns(transformed_table)


def calc_entropy(words):
	for word in words:
		sql = ''''''


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
