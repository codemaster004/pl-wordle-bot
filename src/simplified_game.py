import json


def generate_easy_data(n):
	with open("data/words.json") as file:
		data = json.load(file)
		words = data['slowa']
	
	simple_word = sorted(list(set([word[:4] for word in words])))
	print(len(simple_word))
	
	with open('data/simple_word.json', 'w') as file:
		json.dump({'slowa': simple_word}, file)


if __name__ == '__main__':
	generate_easy_data(0)
