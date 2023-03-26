import json
import random


with open("data/words.json") as file:
	data = json.load(file)
	words = data["slowa"]

letters = list(set([word[:1] for word in words]))
letters.sort()

for char in letters:
	filtered_words = [word for word in words if word[0] == char]
	# with open(f"data/letters/{char}.json", "w") as file:
	# 	json.dump({'slowa': filtered_words}, file, ensure_ascii=False)
		
	print(char, len(filtered_words), sep=': ')
	print(f'    To remove: {int((len(words) - 20_001) * len(filtered_words)/len(words))}')
	with open(f'data/letters/{char}.json') as file:
		data = json.load(file)
		char_words = data['slowa']
		n = len(char_words) - int(20_000 * len(filtered_words) / len(words))
		print(f'    Left to remove: {n}')
		
		# for i in range(n):
		# 	char_words.remove(random.choice(char_words))
	
	# with open(f'data/letters/{char}.json', 'w') as file:
	# 	json.dump({'slowa': char_words}, file, ensure_ascii=False)


shorter_list = []
for char in letters:
	with open(f'data/letters/{char}.json') as file:
		data = json.load(file)
		char_words = data['slowa']
		shorter_list.extend(char_words)

print(len(shorter_list))
with open("data/short_words.json", 'w') as file:
	json.dump({'slowa': shorter_list}, file)
