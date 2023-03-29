import redis
import json


redis_patterns = redis.Redis(host='localhost', port=6379, db=1)

VISUAL_WORD = 'zarys'

with open('data/words.json') as file:
	words = json.load(file)['slowa']

n = len(words)

pattern_chart_data = []

pattern_distribution = redis_patterns.hgetall(VISUAL_WORD)
for pattern, pattern_words in pattern_distribution.items():
	encoded_pattern = pattern.decode('utf-8')
	int_pattern = [int(char) for char in encoded_pattern if char.isdigit()]
	filtered_word = json.loads(pattern_words)
	pattern_chart_data.append([int_pattern, len(filtered_word)])

pattern_chart_data.sort(key=lambda x: x[1], reverse=True)

with open('web/chart_data.js', 'w') as file:
	file.write("const jsonPatterns = '")
	
with open('web/chart_data.js', 'a') as file:
	json.dump({'word': VISUAL_WORD, 'count': len(words), 'patterns': pattern_chart_data}, file)
	
with open('web/chart_data.js', 'a') as file:
	file.write("';")
