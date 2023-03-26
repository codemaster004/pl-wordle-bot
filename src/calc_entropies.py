import time

import redis
import json
import threading
import numpy as np
from datetime import datetime

from main import create_pattern_chart


redis_sorted = redis.Redis(host='localhost', port=6379, db=0)
redis_patterns = redis.Redis(host='localhost', port=6379, db=1)
# redis_entropies = redis.Redis(host='localhost', port=6379, db=4)
# redis_distribution = redis.Redis(host='localhost', port=6379, db=5)


def calc_entropy_for_words(word_list):
	for word in word_list[:1]:
		start = time.perf_counter()
		pattern_distribution = redis_patterns.hgetall(word)
		pattern_distribution = {k.decode('utf-8'): json.loads(v) for k, v in pattern_distribution.items()}
		# print(pattern_distribution)
		score = create_pattern_chart(word, word_list, pattern_distribution)
		end = time.perf_counter()
		print(f"Done in {(end - start) * 1000:0.0f} ms")
		print(word, score)
		redis_sorted.zadd('firstEntropy', {word: score})
		# patterns = dist['patterns']
		# print(f'[{datetime.now().strftime("%H:%M:%S")}] Thread {n}: Calculation Finished for "{dist["key"]}" with a result of {round(dist["entropy"], 3)} Bits')
		
		# We want to save both probabilities for each one and ist entropy
		# redis_distribution.hset(dist['key'].upper(), mapping=patterns)
		# redis_entropies.set(dist['key'].upper(), dist['entropy'])
		# redis_sorted.zadd('entropy', {dist['key'].upper(): dist['entropy']})


def calc_rest_of_entropies():
	# Read word from file
	# with open("data/simple_words.json") as file:
	# 	data = json.load(file)
	# 	words = data['slowa'][:]
	
	# Read all the words we have already done the calculation for.
	calculate_words = redis_patterns.keys('*')
	# decode utf-8 because .keys() return value as bits
	calculate_words = [word.decode('utf-8').lower() for word in calculate_words]
	
	# Run the calculation for them
	# Now i have to pick one with the highest entropy. so calculate the entropy.
	calc_entropy_for_words(calculate_words)


if __name__ == '__main__':
	calc_rest_of_entropies()
