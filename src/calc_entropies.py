import redis
import json
import threading
import numpy as np
from datetime import datetime

from main import create_pattern_chart

redis_sorted = redis.Redis(host='localhost', port=6379, db=0)
redis_entropies = redis.Redis(host='localhost', port=6379, db=1)
redis_distribution = redis.Redis(host='localhost', port=6379, db=2)


def calc_entropy_for_words(word_list, all_words, n=0):
	for word in word_list:
		dist = create_pattern_chart(word, all_words)
		patterns = dist['patterns']
		print(f'[{datetime.now().strftime("%H:%M:%S")}] Thread {n}: Calculation Finished for "{dist["key"]}" with a result of {round(dist["entropy"], 3)} Bits')
		
		# We want to save both probabilities for each one and ist entropy
		redis_distribution.hset(dist['key'].upper(), mapping=patterns)
		redis_entropies.set(dist['key'].upper(), dist['entropy'])
		redis_sorted.zadd('entropy', {dist['key'].upper(): dist['entropy']})


def calc_rest_of_entropies():
	# Read word from file
	with open("data/words.json") as file:
		data = json.load(file)
		words = data['slowa'][:]
	
	# Read all the words we have already done the calculation for.
	calculate_words = redis_entropies.keys('*')
	# decode utf-8 because .keys() return value as bits
	calculate_words = [word.decode('utf-8').lower() for word in calculate_words]
	
	# Find what words are missing
	missing_words = list(set(words) - set(calculate_words))
	missing_words.sort()
	print(len(missing_words), "are missing!")
	
	# Run the calculation for them
	
	n = 5
	# Divide all missing words into N equal groups
	words_chunks = np.array_split(missing_words, n)
	
	threads = []
	for i in range(n):
		t = threading.Thread(target=calc_entropy_for_words, args=(words_chunks[i], words, i))
		threads.append(t)
		t.start()

	# Wait for all threads to finish
	for t in threads:
		t.join()
	
	# i = 4
	# calc_entropy_for_words(words_chunks[i], words)


if __name__ == '__main__':
	calc_rest_of_entropies()
