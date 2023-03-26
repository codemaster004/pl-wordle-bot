import json


def generate_easy_data(n):
	with open("data/words.json") as file:
		data = json.load(file)
		words = data['slowa']
	
	simple_word = sorted(list(set([word[:n] for word in words])))
	print(len(simple_word))
	
	with open(f'data/{n}_letter_words.json', 'w') as file:
		json.dump({'slowa': simple_word}, file)


if __name__ == '__main__':
	generate_easy_data(4)
