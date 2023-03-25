import redis
import json

from main import create_pattern_chart

redis_sorted = redis.Redis(host='localhost', port=6379, db=0)
redis_entropies = redis.Redis(host='localhost', port=6379, db=1)
redis_distribution = redis.Redis(host='localhost', port=6379, db=2)


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
	for word in missing_words:
		dist = create_pattern_chart(word, words)
		patterns = dist['patterns']
		print(f'Calculation Finished for "{dist["key"]}" with a result of {round(dist["entropy"], 3)} Bits')
		
		# We want to save both probabilities for each one and ist entropy
		redis_distribution.hset(dist['key'].upper(), mapping=patterns)
		redis_entropies.set(dist['key'].upper(), dist['entropy'])
		redis_sorted.zadd('entropy', {dist['key'].upper(): dist['entropy']})


if __name__ == '__main__':
	calc_rest_of_entropies()
